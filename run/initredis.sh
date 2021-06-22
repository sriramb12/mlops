function init()
{
redis-cli set root "./run/"
redis-cli set logFolder "./run/log/"
redis-cli set appFolder "./run/bin/"
}
init

function show()
{
redis-cli get root
redis-cli get logFolder
redis-cli get appFolder
}
echo these are variables for mlapp
show
