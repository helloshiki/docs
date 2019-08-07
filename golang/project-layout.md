# golang项目结构
https://github.com/golang-standards/project-layout

###### 如何写出优雅的 Golang 代码 https://draveness.me/golang-101

## api
* OpenAPI/Swagger specs, JSON schema files, protocol definition files. 
  * /api/protobuf-spec 
  * /api/protobuf-spec/oceanbookpb/oceanbook.pb.go
## assets          
* Other assets to go along with your repository (images, logos, etc)
## build           
* Packaging and Continuous Integration.
## cmd             
* Main applications, invokes the code from the /internal and /pkg
  * /cmd/myapp
  * /cmd/server/main.go
## configs         
* Configuration file templates or default configs.
## deployments     
* IaaS, PaaS, system and container orchestration deployment configurations and templates 
  * docker-compose
  * kubernetes/helm
## docs            
* Design and user documents (in addition to your godoc generated documentation).
## examples        
* Examples for your applications and/or public libraries
## githooks        
* Git hooks.
## init            
* System init (systemd, upstart, sysv) and process manager/supervisor (runit, supervisord) configs.
## internal        
* Private application and library code
  * /internal/app/myapp
  * /internal/pkg/myprivlib
## pkg             
* Library code that's ok to use by external applications
  * /pkg/mypubliclib
## scripts         
* Scripts to perform various build, install, analysis, etc operations.
## test            
* Additional external test apps and test data. 
  * /test/data
## third_party     
* External helper tools, forked code and other 3rd party utilities  
  * Swagger UI
## tools           
* Supporting tools for this project. Note that these tools can import code from the /pkg and /internal directories.
## vendor
## web             
* Web application specific components
## website         
* This is the place to put your project's website data if you are not using Github pages.
## .gitignore
## LICENSE.md
## Makefile
## README.md