import sh
import re
import schedule
import logging
import os
import requests
import time
import json

alarms = dict()

config = {
    "check_interval": 10,
    "report_interval": 30,
    "max_cpu": 92,
    "max_mem": 92,
    "max_disk": 92,
    "sc_keys": [],
    "title": "Alert"
}


def watch_disk():
    log = logging.getLogger('alert')

    def list_disk_overseed(max):
        content = sh.bash("-c", "df -h | grep -v -E 'tmpfs|shm'")

        for s in content.strip().split("\n"):
            # /dev/sdb2        94G   88G  2.0G  98% /
            tokens = re.split("[ \t]+", s)
            if len(tokens) < 5:
                log.error("bad df: {}", s)
                continue

            used = tokens[4]
            if not used.endswith("%"):
                log.error("bad df: {}", s)
                continue

            percent = int(used[:-1])
            if percent < max:
                continue

            return content
        return None

    try:
        max_disk = config["max_disk"]
        log.debug("check disk, max:{}".format(max_disk))
        res = list_disk_overseed(max_disk)

        if len(res) == 0:
            return

        s = "\n".join(res)
        alarms["disk"] = s
        log.warning("disk {}".format(s))
    except Exception as e:
        log.exception(e)


def watch_mem():
    log = logging.getLogger('alert')

    def list_mem_overseed(max):
        '''
                              total        used        free      shared  buff/cache   available
        Mem:                16343112    11592380      246748      701876     4503984     3565948
        Swap:               16687100     2756180    13930920
        '''
        c = sh.bash("-c", "free | grep Mem")
        s = str(c)
        tokens = re.split("[ \t]+", s.strip())
        if len(tokens) != 7:
            log.error("bad free: {}", s)
            return None

        total = int(tokens[1])
        available = int(tokens[-1])
        used = (total - available)/total*100
        if used <= max:
            return None

        c = sh.bash("-c", "free -h")
        return str(c)

    try:
        max_mem = config["max_mem"]
        log.debug("check mem, max:{}".format(max_mem))

        res = list_mem_overseed(max_mem)
        if not res:
            return

        alarms["mem"] = res
        log.warning("mem {}".format(res))
    except Exception as e:
        log.exception(e)


def watch_cpu():
    log = logging.getLogger('alert')

    def list_overseed(max):
        '''
        Average:     CPU    %usr   %nice    %sys %iowait    %irq   %soft  %steal  %guest  %gnice   %idle
        Average:     all   24.02    0.00   17.66    0.08    0.00    0.25    0.00    0.00    0.00   57.98
        '''
        c = sh.bash("-c", "mpstat -P ALL 5 1")
        s = str(c)
        matchObj = re.search(r'(Average:\s+all.*)\n', s)
        if not matchObj:
            log.error("bad mpstat: {}", s)
            return

        line = matchObj.group()
        tokens = line.split()
        used = 100 - float(tokens[-1])
        if used <= max:
            return None
        return s

    try:
        max_cpu = config["max_cpu"]
        log.debug("check cpu, max:{}".format(max_cpu))

        res = list_overseed(max_cpu)
        if not res:
            return

        alarms["cpu"] = res
        log.warning("cpu {}".format(res))
    except Exception as e:
        log.exception(e)


def report():
    global alarms
    if len(alarms) == 0:
        return

    m = alarms
    alarms = dict()

    des = []
    for k, s in m.items():
        desc = '#{}\n```\n{}\n```'.format(k, s)
        des.append(desc)

    content = "\n".join(des)
    send_report(content)


def send_report(s):
    sc_keys = config["sc_keys"]
    title = config["title"]
    data = {"text": title, "desp": s}

    logger = logging.getLogger('alert')
    for key in sc_keys:
        url = "https://sc.ftqq.com/{}.send".format(key)
        requests.post(url, data=data)
        logger.warning("send to {} ok".format(key))


def setup_logger():
    logger = logging.getLogger('alert')
    log_level = os.getenv("LOG_LEVEL", "DEBUG")

    logger.setLevel(log_level)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s %(filename)s:%(lineno)d - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)

    fh = logging.FileHandler('/tmp/alert.log')
    fh.setLevel(logging.WARN)
    fh.setFormatter(formatter)

    logger.addHandler(ch)
    logger.addHandler(fh)


last_url_content = ""


def parse_url():
    url = os.getenv("ALERT_URL")
    if not url:
        return

    log = logging.getLogger('alert')
    log.debug("check url: {}".format(url))

    try:
        global last_url_content

        res = requests.get(url)
        content = res.content.decode()
        if content == last_url_content:
            return

        log.info("alert.json change {} -> {}".format(last_url_content, content))
        new_conf = json.loads(content)

        if last_url_content != "":
            exit_keys = ["check_interval", "report_interval", "title"]
            for k in exit_keys:
                if config[k] != new_conf[k]:
                    log.warning("{} change, exit".format(k))
                    exit(0)

        config.update(new_conf)

        log.info("new conf {}".format(json.dumps(config, indent="  ")))
        last_url_content = content

    except Exception as e:
        log.exception(e)


def parse_env():
    s = os.getenv("MAX_DISK_PERCENT")
    if s:
        config["max_disk"] = float(s)

    s = os.getenv("MAX_MEM_PERCENT")
    if s:
        config["max_mem"] = float(s)

    s = os.getenv("MAX_CPU_PERCENT")
    if s:
        config["max_cpu"] = float(s)

    s = os.getenv("CHECK_INTERVAL")
    if s:
        config["check_interval"] = int(s)

    s = os.getenv("REPORT_INTERVAL")
    if s:
        config["report_interval"] = int(s)

    s = os.getenv("ALERT_TITLE")
    if s:
        config["title"] = s

    s = os.getenv("ALERT_LIST")
    if s:
        sc_keys = dict()
        tokens = s.split(",")
        for k in tokens:
            k = k.strip()
            if len(k) > 5:
                sc_keys[k] = 1
        config["sc_keys"] = [k for k in sc_keys.keys()]


if __name__ == "__main__":
    setup_logger()

    log = logging.getLogger('alert')
    log.info("start")

    parse_env()
    parse_url()

    check_interval = config["check_interval"]
    report_interval = config["report_interval"]
    schedule.every(check_interval).minutes.do(watch_disk)
    schedule.every(check_interval).minutes.do(watch_mem)
    schedule.every(check_interval).minutes.do(watch_cpu)
    schedule.every(report_interval).minutes.do(report)
    schedule.every(5).minutes.do(parse_url)

    while True:
        schedule.run_pending()
        time.sleep(1)
