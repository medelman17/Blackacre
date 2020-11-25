package main

import (
	"blackacre/api"
	_ "blackacre/docs"
	"flag"
	"fmt"
	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
	swaggerFiles "github.com/swaggo/files"
	ginSwagger "github.com/swaggo/gin-swagger"
	"google.golang.org/grpc"
)

var (
	addr        string
	port        string
	apiLocation string
)

func init() {
	flag.StringVar(&addr, "server", "127.0.0.1:9999", "gRPC server address")
	flag.StringVar(&port, "port", "8080", "API Port")
	flag.Parse()
	apiLocation = fmt.Sprintf(":%s", port)
}



// @title Blackacre NLP
// @version 0.0.1
// @description This is a sample Blackacre server


// @contact.name Michael Edelman
// @contact.url https://twitter.com/edelman215
// @contact.email michael@fabulas.io

// @license.name Apache 2.0
// @license.url http://www.apache.org/licenses/LICENSE-2.0.html

// @host localhost:8080
// @BasePath /
func main() {
	conn, err := grpc.Dial(addr, grpc.WithInsecure())
	defer conn.Close()

	if err != nil {
		panic(err)
	}


	router := gin.Default()

	router.Use(func(c *gin.Context) {
		c.Set("Connection",conn)
	})

	config := cors.DefaultConfig()

	config.AllowAllOrigins = true

	router.Use(cors.New(config))

	swaggerURL := ginSwagger.URL("http://localhost:8080/swagger/doc.json")
	router.GET("/swagger/*any",ginSwagger.WrapHandler(swaggerFiles.Handler,swaggerURL))

	router.GET("/health/api", api.HandleAPIHealthCheck)
	router.GET("/health/server", api.HandleServerHealthCheck)

	router.POST("/sentence/segment", api.HandleSentenceSegmentRequest)



	router.Run(apiLocation)

}