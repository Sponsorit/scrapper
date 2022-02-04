
sudo docker build -t sponsorit/scrap-service:secondHalf .
sudo docker tag sponsorit/scrap-service:secondHalf 346287969518.dkr.ecr.eu-central-1.amazonaws.com/scrap-service:secondHalf
sudo docker push 346287969518.dkr.ecr.eu-central-1.amazonaws.com/scrap-service:secondHalf