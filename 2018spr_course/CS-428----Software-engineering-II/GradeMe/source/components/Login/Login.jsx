import React, { Component } from 'react'
import { Button, Input, Card } from 'semantic-ui-react'
import { Link, Redirect } from 'react-router-dom'
import { withRouter } from 'react-router'
import axios from 'axios'

import styles from './Login.scss'
import * as _CONFIG from '../_config/Config.js'

class Login extends Component {

    constructor() {
        super();

        this.state = {
            user: {
                password: '',
                email: ''
            },
            redirect: false,
            message: ''
        }

        this.onSubmit = this.onSubmit.bind(this);
        this.onChangeEmail = this.onChangeEmail.bind(this);
        this.onChangePassword = this.onChangePassword.bind(this);
    }

    onSubmit(e) {
        e.preventDefault();
        let component = this;
        const email = encodeURIComponent(this.state.user.email);
        const password = encodeURIComponent(this.state.user.password);
        const formData = `email=${email}&password=${password}`;
        axios.post(_CONFIG.devURL + '/login', formData)
          .then(function (response) {
            console.log(response);
//            location.href = '/dashboard';
            component.setState({
                redirect: true,
                userDetails: response.data
            })
          })
          .catch(function (error) {
            console.log(error);
            component.setState({
                    message: 'Incorrect name or password'
                })
          });



        // const email = encodeURIComponent(this.state.user.email);
        // const password = encodeURIComponent(this.state.user.password);
        // const formData = `email=${email}&password=${password}`;

        // // create an AJAX request (This should probably done with Axios instead)
        // const xhr = new XMLHttpRequest();
        // xhr.open('post', _CONFIG.devURL);
        // xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
        // xhr.responseType = 'json';
        // xhr.addEventListener('load', () => {
        //     if (xhr.status === 200) {
        //         location.href = '/dashboard';

        //     } else {
        //         this.setState({
        //             message: 'Incorrect name or password'
        //         })
        //     }
        // });
        // xhr.send(formData);
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

    render() {
        return(
            <div className="wrapper-login">
                <div className="ui container">
                  <div className="ui large inverted secondary network menu">
                    <Link to="/" className="item" id="logo">GradeMe</Link>
                  </div>
                </div>
                <form className="Login" action="/" onSubmit={this.onSubmit}>
                    <Card className="Login__content">
                        <div>
                            <h1>Login</h1>
                            <Input label="Email" onChange={this.onChangeEmail} />
                            <br/><br/>
                            <Input type="password" label="Password" onChange={this.onChangePassword} />
                            <br/><br/>

                            <p>{this.state.message}</p>
                            <Input type="submit" id="theme-blue"/>
                            <h4>No account yet? Click <Link to="/register" name="signup">here</Link> to Register!</h4>
                        </div>
                    </Card>
                </form>
            </div>
        )
    }
}

export default Login
