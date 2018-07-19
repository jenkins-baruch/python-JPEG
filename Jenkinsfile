pipeline {
  agent any
environment {
    PATH = "$PATH:/var/lib/jenkins/.local/bin"
  }
  stages {
    stage('status'){
        when { changeRequest target: 'master' }
        steps{
            githubNotify(status: 'PENDING', description: 'Wait a minute until I finish testing.')
        }
    }
    stage('environment') {
      steps {
        sh 'touch $WORKSPACE/nosetests.xml'
        echo 'Generate requirements file'
        sh 'pipreqs --force $WORKSPACE/'
        sh 'pip3 install --quiet -r $WORKSPACE/requirements.txt' 
      }
    }
    stage('test'){
        steps{
            sh "FILES=`ls -dm *.py | tr -d ' ' | tr -d '.py'`"
            sh 'nosetests --with-coverage --cover-package=$FILES --cover-erase --cover-inclusive --cover-min-percentage=80'
        }
    }
  }
}