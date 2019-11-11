package main

import (
	"bufio"
	"bytes"
	"encoding/binary"
	"encoding/json"
	"fmt"
	"io"
	"io/ioutil"
	"log"
	"net"
	"os"
	"os/exec"
	"strconv"
	"strings"
	"sync"
	"time"
)

/*
One thread takes a task at a time
a task is a command and a server
*/
type job struct {
	command  string
	serverId int
}

/*
Not used in this mp. It can serve as a thread that
takes in command from stdin constantly
*/
func takeCommand(c chan job) {
	reader := bufio.NewReader(os.Stdin)
	for {

		fmt.Print("Command: ")
		text, _ := reader.ReadString('\n')

		for i := 0; i < numOfServer; i++ {
			temp := job{command: text, serverId: i}
			c <- temp
		}

		if text == "STOP" {
			break
		}
	}
}

/*
Not used in this mp and for testing purpose only
It calls server to send back the whole file, and then it saves
it locally and do the query
*/
func fileCollector(channel chan job) {
	timeoutDuration := 5 * time.Second
	for {
		currentJob := <-channel
		if currentJob.command == "STOP" {
			break
		}
		mutexState.Lock()
		if State[currentJob.serverId] == 0 {
			mutexState.Unlock()
			continue
		}
		mutexState.Unlock()

		conn := Connection[currentJob.serverId]
		fmt.Printf("Talking to %s\n", conn.RemoteAddr().String())
		fmt.Fprintf(conn, "SYN\n")

		reader := bufio.NewReader(conn)

		var buf1 [8]byte
		var err error

		conn.SetReadDeadline(time.Now().Add(timeoutDuration))
		_, err = io.ReadFull(reader, buf1[:])
		if err != nil {
			fmt.Println("Time out on machine %d\n", currentJob.serverId)
			mutexState.Lock()
			State[currentJob.serverId] = 0
			mutexState.Unlock()
			continue
		}

		var size int
		size = int(binary.BigEndian.Uint64(buf1[:]))
		fmt.Printf("received byte length %d\n", size)
		buf := &bytes.Buffer{}
		smallBuf := make([]byte, 256)
		fmt.Fprintf(conn, "ACK\n")

		for buf.Len() != size {
			var n int
			var err error
			conn.SetReadDeadline(time.Now().Add(timeoutDuration))
			n, err = reader.Read(smallBuf)
			if err != nil {
				fmt.Println("Time out on machine %d\n", currentJob.serverId)
				mutexState.Lock()
				State[currentJob.serverId] = 0
				mutexState.Unlock()
				break
			}

			buf.Write(smallBuf[:n])
		}
		mutexState.Lock()
		if State[currentJob.serverId] == 0 {
			mutexState.Unlock()
			continue
		}
		mutexState.Unlock()
		localFileName := "tempFile" + strconv.Itoa(currentJob.serverId)
		localFile, err := os.Create(localFileName)
		check(err)
		_, err = localFile.WriteString(buf.String())
		check(err)
		localFile.Close()
		parts := strings.Fields(currentJob.command)
		head := parts[0]
		fmt.Printf(parts[len(parts)-1])
		parts[len(parts)-1] = localFileName
		parts = parts[1:len(parts)]
		cmd := exec.Command(head, parts...)
		out, err := cmd.CombinedOutput()
		check(err)
		syncStdout.Println(string(out))
	}
}

/*
Main worker thread. Every loop it tries to fetch a new task(command and
server), then it talks to the server and read its output
*/
func handleConnection(channel chan job) {

	//two different timeout values
	timeoutDurationSize := 10 * 60 * time.Second
	timeoutDuration := 10 * time.Second
	for {
		currentJob := <-channel
		if currentJob.command == "STOP" {
			break
		}

		//check if the machine is alive
		mutexState.Lock()
		if State[currentJob.serverId] == 0 {
			mutexState.Unlock()
			continue
		}
		mutexState.Unlock()
		conn := Connection[currentJob.serverId]
		fmt.Printf("Talking to %s\n", conn.RemoteAddr().String())
		fmt.Fprintf(conn, currentJob.command)
		if strings.Compare(currentJob.command, "TEST\n") == 0 {
			continue
		}
		reader := bufio.NewReader(conn)

		//Read the size of output
		var buf1 [8]byte
		var err error
		conn.SetReadDeadline(time.Now().Add(timeoutDurationSize))
		_, err = io.ReadFull(reader, buf1[:])
		if err != nil {
			//check(err)
			fmt.Println("Time out on machine %d\n", currentJob.serverId)
			mutexState.Lock()
			State[currentJob.serverId] = 0
			mutexState.Unlock()
			continue
		}

		var size int

		size = int(binary.BigEndian.Uint64(buf1[:]))
		//start := time.Now()

		fmt.Printf("received byte length %d\n", size)

		buf := &bytes.Buffer{}
		smallBuf := make([]byte, 256)
		fmt.Fprintf(conn, "ACK\n")

		//Read the actual output, read in small buffer and then move to big buffer
		for buf.Len() != size {
			var n int
			var err error
			conn.SetReadDeadline(time.Now().Add(timeoutDuration))
			n, err = reader.Read(smallBuf)
			if err != nil {
				panic(err)
				fmt.Println("Time out on machine %d\n", currentJob.serverId)
				mutexState.Lock()
				State[currentJob.serverId] = 0
				mutexState.Unlock()
				break
			}

			buf.Write(smallBuf[:n])
		}
		mutexState.Lock()
		if State[currentJob.serverId] == 0 {
			mutexState.Unlock()
			continue
		}

		mutexState.Unlock()

		//Write to syncronized stdout
		if testMode {
			localFileName := "vm" + strconv.Itoa(currentJob.serverId+1) + "Output.txt"
			localFile, err := os.Create(localFileName)
			check(err)
			_, err = localFile.WriteString(buf.String())
			check(err)
			localFile.Close()
		} else {
			syncStdout.Println("vm" + strconv.Itoa(currentJob.serverId+1) + ":" + buf.String())
		}
		//fmt.Println("Total query time", time.Since(start))
	}
}

/*
Used for parsing JSON configuration
*/
type Configuration struct {
	NumOfServer int `json:"numOfServer"`
	NumOfThread int `json:"numOfThread"`
	Server      []struct {
		Addr string `json:"Addr"`
		Port string `json:"Port"`
	} `json:"Server"`
}

/*
Global variables
*/
var Connection []net.Conn
var syncStdout = log.New(os.Stdout, "", 0)
var numOfServer int
var numOfThread int
var Port []string
var Addr []string
var State []int
var mutexState = &sync.Mutex{}
var testMode bool

/*
Check error
*/
func check(e error) {
	if e != nil {
		panic(e)
	}
}

/*
Function that reads JSON and parse them into global variables
*/

func readConfig() {
	jsonFile, err := os.Open("./Config.json")
	check(err)
	byteValue, err := ioutil.ReadAll(jsonFile)
	check(err)
	var conf Configuration
	json.Unmarshal(byteValue, &conf)
	numOfServer = conf.NumOfServer
	numOfThread = conf.NumOfThread
	Port = make([]string, numOfServer)
	Addr = make([]string, numOfServer)
	Connection = make([]net.Conn, numOfServer)
	State = make([]int, numOfServer)
	for i := 0; i < numOfServer; i++ {
		Port[i] = conf.Server[i].Port
		Addr[i] = conf.Server[i].Addr
		//fmt.Printf(Addr[i])
	}
	defer jsonFile.Close()
}

func main() {
	arguments := os.Args
	testMode = false
	if len(arguments) == 2 {
		if strings.Compare(arguments[1], "-t") == 0 {
			fmt.Println("Testing mode")
			testMode = true
		} else {
			fmt.Println("Invalid mode")
			return
		}
	}

	//read in JSON
	readConfig()

	for i := 0; i < numOfServer; i++ {
		if strings.Compare(Addr[i], "127.0.0.1") == 0 {
			serverCommand := exec.Command("go", "run", "./Server.go", Port[i])
			serverCommand.Start()
			defer serverCommand.Process.Kill()
		}
	}

	//connection estalished
	var err error
	for i := 0; i < numOfServer; i++ {
		for {
			Connection[i], err = net.Dial("tcp", fmt.Sprintf("%s:%s", Addr[i], Port[i]))
			if err == nil {
				break
			}

		}
	}

	//set up states to be alive
	for i := 0; i < numOfServer; i++ {
		State[i] = 1
	}

	//spawning worker threads
	commands := make(chan job)
	defer close(commands)
	for i := 0; i < numOfThread; i++ {
		go handleConnection(commands)
	}

	if testMode {
		for i := 0; i < numOfServer; i++ {
			temp := job{command: "TEST\n", serverId: i}
			commands <- temp
		}
	}

	//reading from command line constanly and spawn # of servers tasks for each command
	reader := bufio.NewReader(os.Stdin)
	for {

		fmt.Print("Command: ")
		text, _ := reader.ReadString('\n')

		for i := 0; i < numOfServer; i++ {
			temp := job{command: text, serverId: i}
			commands <- temp
		}

		if strings.TrimSpace(string(text)) == "STOP" {
			for i := 0; i < numOfServer; i++ {
				Connection[i].Close()
			}
			break
		}

	}

	syncStdout.Println("END")
}
