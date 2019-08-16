image=$1

if [ "$image" == "" ]
then
echo "Usage: $0 <image-name>"
exit 1
fi

chmod +x lstm/train
chmod +x lstm/serve

# Build the docker image locally with the image name and then push it to ECR
# with the full name.

docker build -t ${image} .