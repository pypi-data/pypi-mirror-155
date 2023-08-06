# Kubernetes MySQL Manager for GIG based clouds.

## Introduction

The **KMM4G** script uses the **MySQL Operator Kubernetes Controller** that can be installed into any existing Kubernetes cluster hosted on **[GIG based clouds](https://gig.tech/)**. Once installed, it will enable users to create and manage production-ready MySQL clusters using a simple declarative configuration format.

Common operational tasks such as backing up databases and restoring from an existing backup are made extremely easy. In short, the **KMM4G** abstracts away the hard work of running MySQL inside Kubernetes.

This script runs on **Kubernetes Clusters** that are hosted on **[GIG based clouds](https://gig.tech/)** which offers IaaS and S3 Cloud for private and public use cases. Check **[GIG based clouds](https://gig.tech/)** to learn more about what they offer.

## Pre-Installing

* You need to have a **Kubernetes Cluster** with **Container Storage Interface (CSI)** which is offered by **[GIG based clouds](https://gig.tech/)**.
* Object storage (S3) provided by **[GIG based clouds](https://gig.tech/)** to store and restore backups.
* You need to have **[Helm Charts](https://helm.sh/)** version 3 installed on your machine.

## Installation Guide

* pip install kmm4g 
* Run command `kmm4g`

### Script Functions 

1. Install MySQL-Operator
2. Create MySQL-Cluster
3. Create Cluster From Existing Backup
4. List Your Clusters
5. Edit Cluster
6. Remove Cluster
7. List Backups
8. Exit

### Step-by-Step Guide

> If you are installing the script for the first time, you need to choose **"Install MySQL-Operator"** option. This command will configure and set up **MySQL-Operator** with the needed packages on your **Kubernetes Clusters**. If you have **MySQL-Operator** installed on your **Kubernetes Clusters**, then you won't be able to install it again.

#### `Create MySQL-Cluster` 

* You can select this option if you want to create a new **MySQL-Cluster**. Then you will need to enter your **MySQL Cluster** data.

| Input | Value |
|-------|-------|
|  **JWT**  | Your JWT token provided on your **[GIG based clouds Account](https://gig.tech/)**.  |
|  **API URL**  | Your **GIG based clouds API URL** (e.g cloud.gig.tech/api/1)  |
|  **Customer ID**  |  Your **[GIG based clouds](https://gig.tech/)** **Customer_ID** provided in your **[GIG based clouds Account](https://gig.tech/)** and also in your **Cloudspace URL**.  |
|  **CloudSpace ID**  |  The ID of your **[GIG based cloudsspace](https://gig.tech/)** that contains your **Kubernetes Cluster**, you can find it in your **Cloudspace URL**.  |
|  **Cluster Name**  |  The name of your **MySQL Cluster** (feel free to name it as you like).  |
|  **Number of Replicas**  |  Number of replicas of your **MySQL Cluster**.  |
|  **Root Password**  |  The root password of your **MySQL Cluster**.  |
|  **MySQL NodePort** [30000-32767]  |  The port to access your **MySQL Cluster** (please select a port between 30000-32767 and make sure that this port isn't used before).  |
|  **Cluster Size (Gi)**  |  Your **MySQL Cluster** size in **GigaBytes**.  |
|  **Enable Auto Backup ?** [yes/no]  |  Select whether you want to enable **auto backup** or not.  |
|  **Backup Schedule** [daily/weekly/monthly/yearly/custom]  |  If you enabled **auto backup**, then you will need to add a schedule for your backup whether daily, weekly, monthly, yearly or even custom.  |
|  **Custom Backup Cronjob**  |  If you selected custom schedule, then you need to set the backup cronjob. Learn more about writing custom cronjobs check **[MySQL Operator Repo](https://github.com/bitpoke/mysql-operator/blob/master/docs/cluster-recurrent-backups.md)**.  |
|  **Number of Backups Limit**  |  The maximum number of backups to be saved (e.g if the limit is 5 then the latest 5 backups will be saved and the older versions will be deleted automatically).  |
|  **Object Storage Endpoint**  |  The domain of your object storage without adding **http** or **https** (e.g example.com).  |
|  **Object Storage Port**  |  The port that you will use to access your object storage.  |
|  **Object Storage Access Key**  |  The access key for your object storage, you cand find it on **GIG based clouds Portal**.  |
|  **Object Storage Secret Key**  |  The secret key for your object storage, you cand find it on **GIG based clouds Portal**.  |
|  **Bucket Name**  |  Enter your bucket name (If you entered a name of **existing bucket** the script will use it. However, if you entered a new name that isn't used before the script will **create a bucket** with the new name for you then use it).  |

For every finished operation you will receive a couple of confirmation messages. At the end, you'll have your **MySQL Cluster** configured.

```bash
Object storage connected
Bucket <BUCKET_NAME> has been created
Creating serverpool...
ServerPool Status 200
Add kubernetes hosts to serverpool...
<KUBERNETES_HOSTS_LIST>
Add hosts to ServerPool Status 200
Creating LoadBalancer...
<LOAD_BALANCER_ID>
Deploying your cluster with auto backup...
NAME: <CLUSTER_NAME>
LAST DEPLOYED: <DEPLOYMENT_DATE_TIME>
NAMESPACE: default
STATUS: deployed
REVISION: 1
TEST SUITE: None

Please wait until the cluster becomes ready...
Access your cluster with port <MYSQL_NODE_PORT> 
```

> You can test whether your **MySQL Cluster** is ready or not using this command `kubectl get pod | grep <CLUSTER_NAME>`.

> Adittionally, to access your **MySQL Cluster** use this command `mysql -uroot -p -h <CLOUDSPACE_PUBLIC_IP> -P <CLUSTER_PORT>`.

#### `Create Cluster From Existing Backup` 

* You can select this option if you want to create a new MySQL-Cluster from an existing backup. Then you will need to enter your **MySQL Cluster** data and the used **Backup** data.

| Input | Value |
|-------|-------|
|  **JWT**  | Your JWT token provided on your **[GIG based clouds Account](https://gig.tech/)**.  |
|  **API URL**  | Your **GIG based clouds API URL** (e.g cloud.gig.tech/api/1)  |
|  **Customer ID**  |  Your **[GIG based clouds](https://gig.tech/)** **Customer_ID** provided in your **[GIG based clouds Account](https://gig.tech/)** and also in your **Cloudspace URL**.  |
|  **CloudSpace ID**  |  The ID of your **[GIG based cloudsspace](https://gig.tech/)** that contains your **Kubernetes Cluster**, you can find it in your **Cloudspace URL**.  |
|  **Cluster Name**  |  The name of your **MySQL Cluster** (feel free to name it as you like).  |
|  **Number of Replicas**  |  Number of replicas of your **MySQL Cluster**.  |
|  **Root Password**  |  The root password of your **MySQL Cluster**. (Should be the same root password as your backup)  |
|  **MySQL NodePort** [30000-32767]  |  The port to access your **MySQL Cluster** (please select a port between 30000-32767 and make sure that this port isn't used before).  |
|  **Cluster Size (Gi)**  |  Your **MySQL Cluster** size in **GigaBytes**.  |
|  **Object Storage Endpoint:**  |  The domain of your object storage without adding **http** or **https** (e.g example.com).  |
|  **Object Storage Port**  |  The port that you will use to access your object storage.  |
|  **Object Storage Access Key**  |  The access key for your object storage, you cand find it on **GIG based clouds Portal**.  |
|  **Object Storage Secret Key**  |  The secret key for your object storage, you cand find it on **GIG based clouds Portal**.  |
|  **Bucket Name**  |  Enter your bucket name (If you entered a name of **existing bucket** the script will use it. However, if you entered a new name that isn't used before the script will **create a bucket** with the new name for you then use it).  |
|  **Enter Your Backup Number**  |  The script will show you the list of backups connected to you object storage endpoint you entered before, just enter the number of the desired backup to be used in this cluster.  |


For every finished operation you will receive a couple of confirmation messages. At the end, you'll have your **MySQL Cluster** configured.

```bash
You select <BackupName>
Creating serverpool...
ServerPool Status 200
Add kubernetes hosts to serverpool...
<KUBERNETES_HOSTS_LIST>
Add hosts to ServerPool Status 200
Creating LoadBalancer...
<LOAD_BALANCER_ID>
Deploying your cluster...
NAME: <CLUSTER_NAME>
LAST DEPLOYED: <DEPLOYMENT_DATE_TIME>
NAMESPACE: default
STATUS: deployed
REVISION: 1
TEST SUITE: None

Please wait until the cluster becomes ready...
Access your cluster with port <MYSQL_NODE_PORT> 
```

> You can test whether your **MySQL Cluster** is ready or not using this command `kubectl get pod | grep <CLUSTER_NAME>`.

> Adittionally, to access your **MySQL Cluster** use this command `mysql -uroot -p -h <CLOUDSPACE_PUBLIC_IP> -P <CLUSTER_PORT>`.

#### `List Clusters` 

* You can select this option if you want to **list all your MySQL Clusters** with their **access ports**.

#### `Edit Cluster` 

* You can select this option if you want to **edit MySQL Clusters**, the script allows you to **change the number of replicas** and **change the backup schedule** (Changing backup schedule is allowed only for **MySQL Clusters** that has **auto backup** enabled).

#### `Remove Cluster` 

* You can select this option if you want to **uninstall a MySQL Cluster**. Just enter the **cluster name** that you want to remove and it will be uninstalled.

#### `List Backups` 

* You can select this option if you want to **list all your backups**.

| Input | Value |
|-------|-------|
|  **Object Storage Endpoint**  | The domain of your object storage without adding **http** or **https** (e.g example.com).  |
|  **Object Storage Port**  |  The port that you will use to access your object storage.  |
|  **Object Storage Access Key**  |  The access key for your object storage, you cand find it on **GIG based clouds Portal**.  |
|  **Object Storage Secret Key**  |  The secret key for your object storage, you cand find it on **GIG based clouds Portal**.  |
|  **Bucket Name**  |  Enter the bucket name that contains your backups.  |
