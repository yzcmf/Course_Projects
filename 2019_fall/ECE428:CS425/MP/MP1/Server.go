package main

import (
	"bufio"
	"encoding/binary"
	"fmt"
	"math/rand"
	"net"
	"os"
	"os/exec"
	"strings"
	"time"
)

const MIN = 1
const MAX = 100

//The following three functions parse commands with quotes
//This returns the matching expression within quotes
func findexpression(s string) string {
	result := ""
	first := false
	first_idx := 0
	idx := 0
	nospace := true
	second_idx := 0
	//get correct indices
	for idx < len(s) {
		if (string(s[idx]) == "\"" && (first == false)) || (string(s[idx]) == "'" && (first == false)) {
			first_idx = idx
			first = true
		} else if string(s[idx]) == "\"" || string(s[idx]) == "'" {
			second_idx = idx
		} else if string(s[idx]) == " " {
			nospace = false
		}
		idx = idx + 1
	}
	idx = first_idx
	for idx <= second_idx {
		result = result + string(s[idx])
		idx = idx + 1
	}
	if first == false || nospace {
		return "NONE"
	} else {
		return result
	}
}

//Returns the matched pattern without quotes
func findtrimmedexpression(s string) string {
	result := ""
	first := false
	first_idx := 0
	idx := 0
	second_idx := 0
	//get correct indices
	for idx < len(s) {
		if (string(s[idx]) == "\"" && (first == false)) || (string(s[idx]) == "'" && (first == false)) {
			first_idx = idx
			first = true
		} else if string(s[idx]) == "\"" || string(s[idx]) == "'" {
			second_idx = idx
		}
		idx = idx + 1
	}
	idx = first_idx + 1
	for idx < second_idx {
		result = result + string(s[idx])
		idx = idx + 1
	}
	return result
}

//this function parses the grep command
func processcmd(s string) []string {

	idx := 0
	//extract expression
	expression := findexpression(s)
	expression_wo_quotes := findtrimmedexpression(s)

	fmt.Println(expression)
	space := false
	for idx < len(expression) {
		if string(expression[idx]) == " " {
			space = true
		}
		idx = idx + 1
	}
	if space == false {
		expression = "NONE"
	}
	fmt.Println(expression)

	idx = 0
	t := strings.Replace(s, expression, "", -1)

	parts := strings.Fields(t)

	var final_parts []string
	if expression == "NONE" {
		fmt.Println("hi")
		final_parts = strings.Fields(s)
	} else {
		final_parts = make([]string, len(parts)+1)

		for idx < len(parts)-1 {
			final_parts[idx] = parts[idx]
			idx = idx + 1

		}

		final_parts[len(parts)-1] = expression_wo_quotes
		final_parts[len(parts)] = parts[len(parts)-1]

	}
	return final_parts

}

//runs the grep command and sends the results back to client
func handleConnection_server(c net.Conn) {
	fmt.Printf("Serving %s\n", c.RemoteAddr().String())

	for {

		// splitting head => g++ parts => rest of the command
		reader := bufio.NewReader(c)
		netData, err := reader.ReadString('\n')
		if err != nil {
			break
		}

		parts := processcmd(netData)
		head := parts[0]
		parts = parts[1:len(parts)]

		//if we are perfoming a unit test
		//generate the log file
		if netData == "TEST\n" {
			cmd := exec.Command("sh", "randomFileGenerator.sh")
			cmd.Start()
			continue
		}

		cmd := exec.Command(head, parts...)

		out, _ := cmd.CombinedOutput()
		//send size of grep output
		var buf [8]byte
		binary.BigEndian.PutUint64(buf[:], uint64(len(string(out))))

		_, err = c.Write(buf[:])
		if err != nil {
			fmt.Println("err:", err)
			break
		}
		ack, _ := reader.ReadString('\n')
		var count int
		count = 0
		fmt.Printf(ack)
		//wait for ack from client
		for ack != "ACK\n" {
			fmt.Printf("Test1")
			for count < len(ack) {
				fmt.Println(ack[count])
				count = count + 1
			}
			ack, _ := reader.ReadString('\n')
			if ack == "ACK\n" {

				break
			}
		}
		//send the output of the command back to the client
		c.Write([]byte(string(string(out))))

	}
	c.Close()

}

//wrapper for server
//here it listens for connections and
//runs commands when contacted
func main() {
	arguments := os.Args
	if len(arguments) == 1 {
		fmt.Println("Please provide a port number!")
		return
	}

	PORT := ":" + arguments[1]
	l, err := net.Listen("tcp4", PORT)
	if err != nil {
		fmt.Println(err)
		return
	}
	defer l.Close()
	rand.Seed(time.Now().Unix())

	for {
		c, err := l.Accept()
		if err != nil {
			fmt.Println(err)
			return
		}
		go handleConnection_server(c)
	}
}
