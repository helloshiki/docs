# ssh
```
ssh server@localhost -NCD "0.0.0.0:8899" -i ~/.ssh/id_rsa
```

# curl
```
curl --socks5 127.0.0.1:8899 www.google.com
```

# golang
```golang
func init() {
	transport := &http.Transport{
		Proxy: func(_ *http.Request) (i *url.URL, e error) {
			return url.Parse("socks5://127.0.0.1:8899")
		},
	}

	client := &http.Client{Transport: transport}
	resp, _ := client.Get("https://www.google.com")

	fmt.Println(resp.StatusCode)
}
```
