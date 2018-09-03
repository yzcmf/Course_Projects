import React, { Component } from 'react'
import PropTypes from 'prop-types';
import { Header, Container, Button, Icon, Table, Modal, TextArea, Input } from 'semantic-ui-react'
import { Link } from 'react-router-dom'
import _ from 'lodash'
import axios from 'axios'
import styles from './Class.scss'

import * as _CONFIG from '../_config/Config.js'

class InstructorClass extends Component {

    // Constructor for component, calls to this component should pass in a classId param (i.e. /class/:id)
    constructor(props){
        super(props);
        this.state = {
            active: this.props.active,
            user: this.props.user,
            modalOpen: false,
            classId: this.props.classId,
            className: this.props.className,
            questionFromInst: "",
            answerOptions: [],
            questionCount: 2,
            additionalOptions: [],
            sortColumn: "Upvotes",
            direction: "descending",
            questions: []
        }
    }

    refreshQuestions = () => {
        if(!this.state.active)
            return;
        let component = this;
        let _url = _CONFIG.devURL + '/question';
        axios.get(_url, {
            params: {
              user: this.state.user,
              course: this.state.classId
            }
          })
          .then(function (response) {
            let result = [];
            response.data.questions.map(function(item, index){
                result.push({upvotes: response.data.upvotes[index], question: item})
            })
            component.setState({
                questions: result
            });
          })
          .catch(function (error) {
            console.log(error);
          });
    }

    componentDidMount(){
        this.refreshQuestions();
        this.interval = setInterval(this.refreshQuestions, 1000);
        console.log("course name")
        console.log(this.state.className)
    }

    componentWillUnmount() {
    // Clear the interval right before component unmount
        clearInterval(this.interval);
    }

    sortTable = clickedColumn => () => {
        let questionData = this.state.questions;
        let currentDirection = this.state.direction;
        if (this.state.sortColumn !== clickedColumn) {
            this.setState({
                sortColumn: clickedColumn,
                questions: _.sortBy(questionData, [clickedColumn]),
                direction: 'descending'
            })
        }else{
            this.setState({
                questions: questionData.reverse(),
                direction: currentDirection === 'ascending' ? 'descending' : 'ascending',
            })
        }
    }

    askQuestion = (event) => {
        event.preventDefault();
        let question = this.state.question;
        this.setState({question:""});
    }

    answeredQuestion = (index) => {
        console.log(index);
        let _url = _CONFIG.devURL + '/ans-question';
        axios.post(_url, {index: index, course: this.state.classId})
        .then(function(response){
            console.log(response);
        }).catch(function(error){console.log(error)});
    }

    saveQuestion = (index) => {
        let _url = _CONFIG.devURL + '/save-question';
        axios.post(_url, {index: index, course: this.state.classId})
        .then(function(response){
            console.log(response);
        }).catch(function(error){console.log(error)});
    }

    generateQuestionRow = (questionObj, index) => {
        return (
            <Table.Row key={index}>
                <Table.Cell textAlign='center'>{questionObj.upvotes}</Table.Cell>
                {/*<Table.Cell textAlign='center'>{questionObj.student}</Table.Cell>*/}
                <Table.Cell>{questionObj.question}</Table.Cell>
                <Table.Cell textAlign='center'>{<img src="https://png.icons8.com/checked/win8/25/000000" className="pointer" onClick={()=>this.answeredQuestion(index)}/>}</Table.Cell>
                <Table.Cell textAlign='center'>{<img src="https://png.icons8.com/clock/win10/30/000000" className="pointer" onClick={()=>this.saveQuestion(index)}/>}</Table.Cell>
            </Table.Row>
        )
    }

    handleOpen = () => this.setState({ modalOpen: true })

    handleClose = () => {
        this.setState({ modalOpen: false });
        //POST Data to students
    }

    addOption = () => {
        let qc = this.state.questionCount + 1;
        console.log('adding!');
        const qns = this.state.additionalOptions;
        this.setState({
            additionalOptions: qns.concat(<Input key={qc} className='instOption' placeholder='Option'/>),
            questionCount: qc
        });
    }

    generateAdditionalOptions = () => {
        return  <Input index={3} className='instOption' placeholder='Option'/>
    }

    toggleSession = () => {
        let active = this.state.active;
        let component = this;
        let _url = _CONFIG.devURL + (active ? "/end-class" : "/start-class");
        axios.post(_url, {course: this.state.classId, user: this.state.user})
        .then(function(response){
            component.setState({
                active: !active
            })
        })
        .catch(function(error){
            console.log(error);
        })
    }

    render() {
        if(!this.state.active){
            return (
                <div className='sessions'>
                <h2 className="class_name"> {this.state.className} </h2>
                <div className="courseID"> Course ID: {this.state.classId}</div>
                <Button className="currentSession" onClick={this.toggleSession}>Start Session</Button>
                </div>
            )
        }
        let sortBy = this.state.sortColumn;
        let currentDirection = this.state.direction;
        return(
            <div>
                <h2 className="class_name"> {this.state.className} </h2>
                <div className="courseID"> Course ID: {this.state.classId}</div>
                <Container className="questionSection">
                    <Modal trigger={<div onClick={this.handleOpen} className="hidden"></div>}
                    open={this.state.modalOpen} onClose={this.handleClose}>
                        <Modal.Header>Post a Question</Modal.Header>
                        <Modal.Content>
                              <TextArea className="instQuestion" placeholder='Your Question Here...' autoHeight rows={3} onChange={(event,data) => this.setState({questionFromInst: data.value})}/>
                              <div className='instQnArea'>
                                  <Input key={0} className='instOption' placeholder='Option'/>
                                  <Input key={1} className='instOption' placeholder='Option'/>
                                  {this.state.additionalOptions.map(function(input, index) {
                                      return input;
                                  })}
                              </div>
                              <Button className='addOption' color='blue' onClick={this.addOption} inverted>Add Option</Button>
                        </Modal.Content>
                        <Modal.Actions>
                          <Button color='green' onClick={this.handleClose} inverted>
                            Ask
                          </Button>
                        </Modal.Actions>
                    </Modal>
                </Container>
                <Container className="questionList">
                    <Table padded striped celled className="questionsTable">
                        <Table.Header className="tableHeader">
                            <Table.Row>
                                <Table.HeaderCell className="pointer" sorted={sortBy === 'Upvotes' ? currentDirection : null} onClick={this.sortTable('upvotes')}>Upvotes</Table.HeaderCell>
                                {/*<Table.HeaderCell sorted={sortBy === 'Asked' ? currentDirection : null} onClick={this.sortTable('student')}>Asked By</Table.HeaderCell>*/}
                                <Table.HeaderCell>Question</Table.HeaderCell>
                                <Table.HeaderCell>Answer</Table.HeaderCell>
                                <Table.HeaderCell>Save</Table.HeaderCell>
                            </Table.Row>
                        </Table.Header>
                        <Table.Body>
                            {this.state.questions.map(this.generateQuestionRow)}
                       </Table.Body>
                    </Table>
                </Container>
                <div className='sessions'>
                <Button className="currentSession" onClick={this.toggleSession}>End Session</Button>
                </div>
            </div>
        )
    }
}

InstructorClass.propTypes = {
    className: PropTypes.string,
    classId: PropTypes.string,
    isInstructor: PropTypes.bool,
    questionFromInst: PropTypes.string,
    questions: PropTypes.array
}

export default InstructorClass
