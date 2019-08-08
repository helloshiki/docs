# 代码提交前，格式化
```shell
goimports -w . 
```
安装方法: 
```
go get golang.org/x/tools/cmd/goimports
```

# 代码提交前，使用检查工具
```shell
golint  ./...
golint dir
golangci-lint run
golangci-lint run dir1 dir2/... dir3/file1.go
```
*golint安装方法:        https://github.com/golang/lint
*golangci-lint安装方法: https://github.com/golangci/golangci-lint

# Go官方编程规范
https://github.com/golang/go/wiki/CodeReviewComments
*Go官方编程规范(中文翻译,省略了很多细节)
http://www.gonglin91.com/2018/03/30/go-code-review-comments/

# Effective Go
https://golang.org/doc/effective_go.html
*Effective Go(中文翻译)
https://www.kancloud.cn/kancloud/effective/72204

# 如何写出优雅的 Golang 代码
https://draveness.me/golang-101
