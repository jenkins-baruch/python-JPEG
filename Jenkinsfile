pipeline {
  agent any
  stages {
    stage('stage1.1') {
      parallel {
        stage('stage1.1') {
          steps {
            sh 'echo "1.1"'
          }
        }
        stage('stage1.2') {
          steps {
            echo '1.2'
          }
        }
      }
    }
    stage('stage2.1') {
      parallel {
        stage('stage2.1') {
          steps {
            echo '2.1'
          }
        }
        stage('2.2') {
          steps {
            echo '2.2'
          }
        }
      }
    }
  }
}