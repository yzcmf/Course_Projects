import React, { Component } from 'react'
import PropTypes from 'prop-types';
import { Header, Container, Button, TextArea, Table , Icon} from 'semantic-ui-react'
import _ from 'lodash'

import axios from 'axios'
import styles from './Class.scss'
import * as _CONFIG from '../_config/Config.js'

class StudentClass extends Component {

    // Constructor for component, calls to this component should pass in a classId param (i.e. /class/:id)
    constructor(props){
        super(props);
        console.log(props);
        this.state = {
            classId: this.props.classId,
            user: this.props.user,
            isActive: this.props.active,
            className: this.props.className,
            studentQuestion: "",
            sortColumn: "Upvotes",
            direction: "descending",
            questions: []
        }
    }

    refreshQuestions = () => {
        if(!this.state.isActive)
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

    checkActive = () => {
        let component = this;
        axios.get(_CONFIG.devURL + '/active').then(function(response){
            component.setState({isActive: (_.indexOf(response.data.activeClasses, component.state.classId)) !== -1})
        }).catch(function(error){console.log(error)});
    }

    componentDidMount(){
        this.refreshQuestions();
        this.interval = setInterval(this.refreshQuestions, 1000);
        this.intervalActive = setInterval(this.checkActive, 3000);
    }

    componentWillUnmount() {
    // Clear the interval right before component unmount
        clearInterval(this.interval);
        clearInterval(this.intervalActive);
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
        let _url = _CONFIG.devURL + "/question"
        let component = this;
        axios.post(_url, {
            question: this.state.studentQuestion,
            user: this.state.user.user,
            course: this.state.classId
        }).then(function(response){
            component.setState({studentQuestion:""});
        }).catch(function(error){
            console.log(error);
        })

    }

    upvoteQuestion = (value, index) => {
        let _url = _CONFIG.devURL + '/upvote';
        axios.post(_url, {course: this.state.classId, index: index})
        .then(function(response){
            console.log(response);
        }).catch(function(error){console.log(error)})
        // let questions = this.state.questions;
        // questions.map(function(entry, index){
        //     if (entry.question === value){
        //         entry.upvotes += 1
        //     }
        // })
        // this.setState({questions: questions})
    }

    generateQuestionRow = (questionObj, index) => {
        return (
            <Table.Row key={index}>
                <Table.Cell textAlign='center'>{questionObj.upvotes}  <img src="https://png.icons8.com/sort-up/win8/64/000000" className="upvote pointer" onClick={()=>this.upvoteQuestion(questionObj.question, index)}/></Table.Cell>
                {/*<Table.Cell textAlign='center'>{questionObj.time}</Table.Cell>*/}
                <Table.Cell>{questionObj.question}</Table.Cell>
            </Table.Row>
        )
    }

    renderActive() {
        let sortBy = this.state.sortColumn;
        let currentDirection = this.state.direction;
        return(
            <div>
                <h2 className="class_name"> {this.state.className} </h2>
                <Container className="questionSection">
                    <h3>Ask A Question</h3>
                    <TextArea value={this.state.studentQuestion} className="question" placeholder='Your Question Here...' autoHeight rows={3} onChange={(event,data) => this.setState({studentQuestion: data.value})}/>
                    <br></br>
                    <Button className="submit_question" onClick={this.askQuestion}>
                        Submit
                    </Button>
                </Container>
                <Container className="questionList">
                    <Table padded striped celled className="questionsTable">
                        <Table.Header className="tableHeader">
                            <Table.Row>
                                <Table.HeaderCell className="pointer" sorted={sortBy === 'Upvotes' ? currentDirection : null} onClick={this.sortTable('upvotes')}>Upvotes</Table.HeaderCell>
                                {/*<Table.HeaderCell sorted={sortBy === 'Time' ? currentDirection : null} onClick={this.sortTable('time')}>Time</Table.HeaderCell>*/}
                                <Table.HeaderCell>Question</Table.HeaderCell>
                            </Table.Row>
                        </Table.Header>
                        <Table.Body>
                            {this.state.questions.map(this.generateQuestionRow)}
                       </Table.Body>
                    </Table>
                </Container>
            </div>
        )
    }
    renderInactive(){
        return(
            <div>
                <h2 className="class_name"> {this.state.className} inactive</h2>
                <h3>Class is currently not active</h3>
            </div>
        )
    }
    render(){
        return(
            <div className={this.state.isActive ? '' : 'inactiveHeader'}>
                {this.state.isActive ? this.renderActive() : this.renderInactive()}
            </div>
        )
    }
}

StudentClass.propTypes = {
    classId: PropTypes.string,
    isActive: PropTypes.bool,
    isInstructor: PropTypes.bool,
    studentQuestion: PropTypes.string,
    questions: PropTypes.array
}

export default StudentClass
