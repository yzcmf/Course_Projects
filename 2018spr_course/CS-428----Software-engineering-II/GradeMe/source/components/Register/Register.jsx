import React, { Component } from 'react'
import { Button, Input, Card } from 'semantic-ui-react'
import { Link } from 'react-router-dom'
import axios from 'axios'

import styles from './Register.scss'
import * as _CONFIG from '../_config/Config.js'


class Register extends Component {
    constructor(props) {
        super(props);

        this.state = {
            user: {
                name: '',
                password: '',
                email: '',
                courses: []
            },
            inputList: [],
            showStudent: false,
            showInstructor: false,
            message: ''
        };
        this.ChangeToStudent = this.ChangeToStudent.bind(this);
        this.ChangeToInstructor = this.ChangeToInstructor.bind(this);
        this.onSubmit = this.onSubmit.bind(this);
        this.onChangeName = this.onChangeName.bind(this);
        this.onChangeEmail = this.onChangeEmail.bind(this);
        this.onChangePassword = this.onChangePassword.bind(this);
        this.onChangeCourses = this.onChangeCourses.bind(this);
        this.onAddBtnClick = this.onAddBtnClick.bind(this);
    }

    onSubmit(e) {
        e.preventDefault();

        if(this.state.showInstructor===true){
            axios.post(_CONFIG.devURL + '/register', {
            name: this.state.user.name,
            email: this.state.user.email,
            password: this.state.user.password,
            is_instructor: this.state.showInstructor
          })
          .then(function (response) {
            console.log(response);
            location.href = '/login';
          })
          .catch(function (error) {
            console.log(error);
            this.setState({
                     message: 'Unable to register'
                 })
          });
        }
        // else{
        //     var id = 0;
        //     for(id = 1; id < this.state.user.courses.length; id++){
        //         axios.put(_CONFIG.devURL + '/add-class', {
        //             course: this.state.user.courses[id]
        //           })
        //           .then(function (response) {
        //             console.log(response);
        //           })
        //           .catch(function (error) {
        //             console.log(error);
        //             this.setState({
        //                      message: 'Unable to register class'
        //                  })
        //           });
        //     }

            axios.post(_CONFIG.devURL + '/register', {
            name: this.state.user.name,
            email: this.state.user.email,
            password: this.state.user.password,
            is_instructor: this.state.showInstructor
          })
          .then(function (response) {
            console.log(response);
            location.href = '/login';
          })
          .catch(function (error) {
            console.log(error);
            this.setState({
                     message: 'Unable to register '
                 })
          });
        }
    
    componentDidMount(){
        if(this.props.location.state !== undefined){
            console.log(this.props);
            if(this.props.location.state.teacher==true){
                this.ChangeToInstructor();
            }
            else if(this.props.location.state.student==true){
                this.ChangeToStudent();
            }
        }

    }
    ChangeToStudent() {
        this.setState({
            showStudent: true,
            showInstructor: false
        });
    }
    ChangeToInstructor() {
        this.setState({
            showStudent: false,
            showInstructor: true
        });
    }
    onChangeName(e) {
        const user = this.state.user;
        user.name = e.target.value;
        this.setState({
            user
        })
    }

    onChangeEmail(e) {
        const user = this.state.user;
        user.email = e.target.value;
        this.setState({
            user
        })
    }

    onChangePassword(e) {
        const user = this.state.user;
        user.password = e.target.value;
        this.setState({
            user
        })
    }
    onChangeCourses(e) {
        const user = this.state.user;
        user.courses = e.target.value;
        this.setState({
            user
        })
    }
    onAddBtnClick(event) {
        const inputList = this.state.inputList;
        this.setState({
            inputList: inputList.concat(<Input label="Course Code" className="pad" onChange={this.onChangeCourses} />)
        });
    }
    render() {
        return(
            <div className="wrapper-register">
                <div className="ui container">
                  <div className="ui large inverted secondary network menu">
                    <Link to="/" className="item" id="logo">GradeMe</Link>
                  </div>
                </div>
                <form className="Register" action="/" onSubmit={this.onSubmit}>
                    <Card className="Register__content">
                        <div>
                            <h1>Register</h1>
                                <br/>
                                <Input label="Name" className = "pad" onChange={this.onChangeName} />
                                <Input label="Email" className = "pad" onChange={this.onChangeEmail} />
                                <Input type="password" label="Password" className = "pad" onChange={this.onChangePassword} />
                                <Input type="password" label="Confirm" className = "pad" onChange={this.onChangePassword} />

                            <p>{this.state.message}</p>
                            <Input type="submit" id="theme-blue"/>
                            <h4>Already registered? Click <Link to="/login" name="login">here</Link> to Log-in!</h4>
                        </div>
                    </Card>
                </form>
            </div>
        )
    }
}
//<Input label="Course Code" className = "pad" onChange={this.onChangeCourses} />
//                                {this.state.inputList.map(function(input, index) {
//                                    return input;
//                                })}
//                                <div className="ui basic button pad" onClick={this.onAddBtnClick}>
//                                  Add Course
//                                </div>
export default Register
