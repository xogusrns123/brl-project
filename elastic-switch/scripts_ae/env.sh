WORK_DIR=$(pwd)

export PYTHONPATH=$WORK_DIR:$PYTHONPATH
# Comment out the following line if there's no need to specify the network interface
# export NCCL_SOCKET_IFNAME=ens5
export NCCL_SOCKET_IFNAME=eno1np0
# Set this as the path to the binary of mpirun
# export MPI_EXEC=/opt/amazon/openmpi/bin/mpirun
export MPI_EXEC=/usr/local/bin/mpirun

# Set this to the directory where you cloned the repo or unzipped the tarball
# BASE_DIR=/home/ubuntu/spot_inference
BASE_DIR=/home/kth/brl/SpotServe

# export MASTER_IP=172.31.6.17
export MASTER_IP=143.248.53.59
export MASTER_PORT=10224
export API_SERVER_PORT=14141
export PARAM_CLIENT_EXEC=${BASE_DIR}/ParamsClient/build/bin/param_client
export FT_INFER_EXEC=${BASE_DIR}/FasterTransformer/build/bin/multi_gpu_gpt_example_iter
