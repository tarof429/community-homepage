def showEnvironment() {
    echo "Showing environment"
    sh "which docker"
    sh "whoami"
    sh "pwd"
}

return this