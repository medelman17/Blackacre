package api

import (
	"context"
	"fmt"
	"github.com/gin-gonic/gin"
	"google.golang.org/grpc"
	"blackacre/pb"
)



//
// @Summary Check health of API layer
// @Produce  json
// @Success 200 {string} string	"ok"
// @Router /health/api [get]
func HandleAPIHealthCheck(c *gin.Context) {

}


type BlackacreServerError struct {
	error string `json:"error"`
}

//
// @Summary Check health of Server layer
// @Produce  json
// @Success 200 {string} string	"ok"
// @Failure 500 {object} BlackacreServerError
// @Router /health/server [get]
func HandleServerHealthCheck(c *gin.Context) {
	conn, exists := c.Get("Connection")
	if !exists {
		panic("Connection not put on context")
	}

	client := pb.NewBlackacreClient(conn.(grpc.ClientConnInterface))

	req := pb.BlackacreHealthCheckRequest{}

	resp, err := client.HealthCheck(context.TODO(),&req)
	if err != nil {
		fmt.Println("ERROR", err)
		c.JSON(500, gin.H{
			"error": "Downstream Blackacre server unavailable",
		})
	}
	fmt.Printf(resp.String())
}



