pipeline {
  agent any
  stages {
      stage('status'){
          when { changeRequest target: 'master' }
          steps{}
      }
    stage('build') {
      steps {
        sh 'pwd'
        sh 'ls'
        sh 'git status'
        githubNotify(status: 'PENDING', description: 'Wait a minute until I finish testing.')
      }
    }
  }
}