package api

import (
	"blackacre/pb"
	"context"
	"github.com/gin-gonic/gin"
	"google.golang.org/grpc"
)




type SentenceSegmenterRequestBody struct {
	Text string `json:"text"`
}

//
// @Summary Segment text into constituent sentences...
// @Accepts json
// @Produce  json
// @Param data body SentenceSegmenterRequestBody true "request body"
// @Success 200 {string} string	"ok"
// @Router /sentence/segment [post]
func HandleSentenceSegmentRequest(c *gin.Context) {
	var req SentenceSegmenterRequestBody

	if c.ShouldBindJSON(&req) == nil {
		conn, exists := c.Get("Connection")
		if !exists {
			panic("Connection not put on context")
		}

		client := pb.NewBlackacreClient(conn.(grpc.ClientConnInterface))

		req := pb.BlackacreSentenceSegmenterRequest{
			Text: req.Text,
		}

		resp, err := client.GetSentences(context.TODO(), &req)
		if err != nil {
			c.Error(err)
			return
		}

		 c.JSON(200, gin.H{
		 	"sentences": resp.Sentences,
		 })
	}

}