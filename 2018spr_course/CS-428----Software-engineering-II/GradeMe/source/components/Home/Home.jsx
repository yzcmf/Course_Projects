import React, { Component } from 'react'
import { Button, Card } from 'semantic-ui-react'
import { Link } from 'react-router-dom'

import styles from './Home.scss'

class Home extends Component {
    render() {
        return(
            <div className="wrapper-home">
                <div className="ui container">
                  <div className="ui large inverted secondary network menu">
                    <Link to="/" className="item" id="logo">GradeMe</Link>
                  </div>
                </div>
                <div className="Home">
                  <div className="ui text container" id = "Home_content">
                    <h1 className="ui header" id="title-clearity">
                        GradeMe
                    </h1>
                    <h2>
                        Better Way to Grade Students
                    </h2>
                    <Link to={{ pathname: '/login', state: { student: true} }} className="item">
                      <div className="ui huge primary button" id="theme-blue" name="login">
                        Login
                      </div>
                    </Link>
                    <Link to={{ pathname: '/register', state: { teacher: true} }} className="item">
                      <div className="ui huge primary button" id="theme-blue" name="signup">
                        Sign Up
                      </div>
                    </Link>
                  </div>
                </div>
            </div>
        )
    }
}

export default Home
