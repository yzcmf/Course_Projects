import React, { Component } from 'react'
import PropTypes from 'prop-types';
import { Header, Button, Table, Grid, Menu, Segment } from 'semantic-ui-react'
import _ from 'lodash'
import { Link, Redirect } from 'react-router-dom'

import styles from './Sessions.scss'
import axios from 'axios'
import * as _CONFIG from '../_config/Config.js'

class Sessions extends Component {

    constructor(props){
        super(props);
        this.state = {
            isActive: this.props.isActive,
            classId: this.props.classId,
            classTitle: this.props.classTitle,
            currentSession: "",
            sessions: [],
            allQuestions: {},
            questions: [],
            user: this.props.user
        }

    }

    parseData = (data) => {
        console.log(data);
        let dates = [];
        let allQuestions = {};
        for (let i = 0; i < data.length; i++){
            if(data[i].active)
                continue
            let sessionEntry = data.length - i + ' - ' + new Date(data[i].date).toDateString();
            dates.push(sessionEntry);
            let sessionQuestions = [];
            let questions = data[i].questions;
            let upvotes = data[i].upvotes;
            let ansQuestions = data[i].answeredQuestions;
            let ansUpvotes = data[i].ansUpvotes;
            let savedQuestions = data[i].savedQuestions;
            let savedUpvotes = data[i].savedUpvotes;
            for(let q = 0; q < questions.length; q++){
                sessionQuestions.push({qn: questions[q], upvotes: upvotes[q]})
            }
            for(let a = 0; a < ansQuestions.length; a++){
                sessionQuestions.push({qn: ansQuestions[a], upvotes: ansUpvotes[a]})
            }
            for(let s = 0; s < savedQuestions.length; s++){
                sessionQuestions.push({qn: savedQuestions[s], upvotes: savedUpvotes[s]})
            }
            allQuestions[sessionEntry] = sessionQuestions
        }
        console.log(dates);
        console.log(allQuestions);
        this.setState({
            sessions: dates,
            currentSession: dates[0],
            allQuestions: allQuestions,
            questions: allQuestions[dates[0]]
        })
    }

    componentDidMount(){
        let _url = _CONFIG.devURL + '/sessions';
        let component = this;
        axios.get(_url, {
            params: {
              course: this.state.classId
            }
          }).then(function(response){
            let data = response.data.sessions.reverse();
            component.parseData(data);
        }).catch(function(error){console.log(error)});
    }

    onCurrentSessionClick = () => {
        this.props.onCurrentClick();
    }

    onSessionClick = (e, { name }) => {
        this.setState({
            currentSession: name,
            questions: this.state.allQuestions[name]
        })
    }

    renderSessions = (item, index) => {
        return(
            <Menu.Item key={index} name={item} active={this.state.currentSession === item} onClick={this.onSessionClick}/>
        )
    }

    generateQuestionRow = (item, index) => {
        return (
            <Table.Row key={index}>
                <Table.Cell textAlign='center'>{item.upvotes}</Table.Cell>
                <Table.Cell>{item.qn}</Table.Cell>
            </Table.Row>
        )
    }



    render(){
        return(
            <div className='sessions'>
                <h3 className='header'>Records for {this.state.classTitle}</h3>
                { this.state.isActive &&
                  <Button className="currentSession" onClick={this.onCurrentSessionClick}>Current Session</Button>
                }
                <Grid>
                    <Grid.Column width={2}>
                      <Menu fluid vertical tabular>
                        {this.state.sessions.map(this.renderSessions)}
                      </Menu>
                    </Grid.Column>

                    <Grid.Column stretched width={14}>
                      <Segment>
                          <Table sortable padded striped celled className="questionsTable">
                              <Table.Header className="tableHeader">
                                  <Table.Row>
                                      <Table.HeaderCell>Upvotes</Table.HeaderCell>
                                      <Table.HeaderCell >Questions</Table.HeaderCell>
                                  </Table.Row>
                              </Table.Header>
                              <Table.Body>
                                  {this.state.questions ? this.state.questions
                                      .sort((a, b) => a.upvotes < b.upvotes)
                                      .map(this.generateQuestionRow) : null}
                              </Table.Body>
                         </Table>
                      </Segment>
                    </Grid.Column>
                </Grid>
            </div>
        )
    }
}

History.propTypes = {
    classId: PropTypes.string,
    isActive: PropTypes.bool,
    sessions: PropTypes.array
}

export default Sessions
