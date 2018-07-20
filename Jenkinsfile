pipeline {
  agent any
environment {
    PATH = "$PATH:/var/lib/jenkins/.local/bin"
  }
  stages {
    // stage('status'){
    //     when { changeRequest target: 'master' }
    //     steps{
    //         githubNotify(status: 'PENDING', description: 'Wait a minute until I finish testing.')
    //     }
    // }
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
            //sh "FILES=`ls -dm *.py | tr -d ' ' | tr -d '.py'`"
            sh "nosetests --with-coverage --cover-package=`ls -dm *.py | tr -d ' ' | tr -d '.py'` --cover-erase --cover-inclusive --cover-min-percentage=80"
            sh "pylint -f parseable *.py | tee pylint.out"
            sh "coverage xml"
        }
    }
    // stage('publish results'){
    //   steps{
    //         cobertura autoUpdateHealth: false, autoUpdateStability: false, coberturaReportFile: '**/coverage.xml', conditionalCoverageTargets: '70, 0, 0', failUnhealthy: false, failUnstable: false, lineCoverageTargets: '80, 0, 0', maxNumberOfBuilds: 0, methodCoverageTargets: '80, 0, 0', onlyStable: false, sourceEncoding: 'ASCII', zoomCoverageChart: false
    //   }
    // }
  }
}