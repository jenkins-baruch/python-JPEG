pipeline {
  agent any
  stages {
    stage('environment') {
      steps {
        sh 'touch $WORKSPACE/nosetests.xml'
        echo 'Generate requirements file'
        sh 'pipreqs --force $WORKSPACE/'
        sh 'pip3 install --quiet -r $WORKSPACE/requirements.txt'
      }
    }
    stage('test') {
      steps {
        sh 'nosetests --with-coverage --cover-package=`ls -dm *.py | tr -d \' \' | tr -d \'.py\'` --cover-erase --cover-inclusive --cover-min-percentage=80 --with-xunit'
        sh 'pylint -f parseable *.py | tee pylint.out'
        sh 'coverage xml'
      }
    }
    stage('publish') {
      steps {
        //junit '**/nosetests.xml'
        cobertura(coberturaReportFile: '**/coverage.xml')
      }
    }
  }
  environment {
    PATH = "$PATH:/var/lib/jenkins/.local/bin"
  }
}