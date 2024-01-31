#!/bin/bash
NAME="python"
docker exec db /bin/bash -c "/workspace/scripts/add_env.sh ${NAME}"