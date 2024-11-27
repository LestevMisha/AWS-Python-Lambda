# Level 1
# Step 1
- Open Terminal
`cd /Users/mishalestev/Desktop/work-2024`
`mkdir aws-complete-setup && code aws-complete-setup`
- Open VS Code Terminal
`touch lambda_function.py`
`cat > lambda_function.py`
- Paste in the content of <code>.txt
- Press `CNTRL` + `D` (2,3 times if needed)

# Step 2
- Choose Python 13 at the bottom menu
`python3.13 -m venv .venv`
- Switch to the .venv (click "Yes/Confirm" for the info pop-up)
`source .venv/bin/activate`
- Quick Check
`python3 --version`
`pip3 --version`
- Install Dependencies
`touch requirements.txt`
`echo "chess
pandas
python-telegram-bot
cairosvg" > requirements.txt`
`pip3 install -r requirements.txt`
- `CMD` + `R` test if script works

# Step 3
`mkdir aws-packages && cd aws-packages`
- Read docs about correct/incorrect OS compatability [docs](https://docs.aws.amazon.com/lambda/latest/dg/lambda-python.html)
**correct** `docker run -it --rm --entrypoint bash -v $(pwd):/var/task public.ecr.aws/lambda/python:3.11`

*incorrect* `docker run -it --rm -v $(pwd):/var/task python:3.13 bash`
- Quick Check
`python3 --version`
`pip3 --version`
- Check that your architecture is `aarch64`
`uname -a`
`pwd`
- `pwd` should show `/var/task` otherwise `cd /var/task`
`mkdir chess/python python-telegram-bot/python cairosvg/python cairosvg/lib`
- We ignore `pandas` since `pandas` is available by default as a layer in AWS Lambda
- Install to each folder its needed dependencies (they will serve as an independent layers later)
`pip3 install --target=/var/task/chess/python chess`
`pip3 install --target=/var/task/python-telegram-bot/python python-telegram-bot`
`pip3 install --target=/var/task/cairosvg/python cairosvg`
- Install external dependencies needed to run cairosvg module (except zip)
**correct** `yum update -y`
**correct**`yum install -y gcc gcc-c++ cairo cairo-devel libffi libffi-devel libjpeg-turbo libpng libpng-devel zip`

*incorrect* `apt-get update`
*incorrect* `apt-get install -y libcairo2 libcairo2-dev libpango1.0-0 libjpeg62-turbo libjpeg62-turbo-dev libpng-dev zip`
- Figure out dependencies for libcairo.so.2
`find /usr -name libcairo.so.2`
- Make sure path is the same as for `libcairo.so.2`
`ldd /usr/lib64/libcairo.so.2`

- Gather a bunch od external dependencies to `/var/task/cairosvg/lib`
<!-- linux-vdso.so.1 -->
**correct** cp /lib64/libcairo.so.2 /var/task/cairosvg/lib
**correct** cp /lib64/libpthread.so.0 /var/task/cairosvg/lib
**correct** cp /lib64/libpixman-1.so.0 /var/task/cairosvg/lib
**correct** cp /lib64/libfontconfig.so.1 /var/task/cairosvg/lib
**correct** cp /lib64/libfreetype.so.6 /var/task/cairosvg/lib
**correct** cp /lib64/libEGL.so.1 /var/task/cairosvg/lib
**correct** cp /lib64/libdl.so.2 /var/task/cairosvg/lib
**correct** cp /lib64/libpng15.so.15 /var/task/cairosvg/lib
**correct** cp /lib64/libxcb-shm.so.0 /var/task/cairosvg/lib
**correct** cp /lib64/libxcb.so.1 /var/task/cairosvg/lib
**correct** cp /lib64/libxcb-render.so.0 /var/task/cairosvg/lib
**correct** cp /lib64/libXrender.so.1 /var/task/cairosvg/lib
**correct** cp /lib64/libX11.so.6 /var/task/cairosvg/lib
**correct** cp /lib64/libXext.so.6 /var/task/cairosvg/lib
**correct** cp /lib64/libz.so.1 /var/task/cairosvg/lib
**correct** cp /lib64/libGL.so.1 /var/task/cairosvg/lib
**correct** cp /lib64/librt.so.1 /var/task/cairosvg/lib
**correct** cp /lib64/libm.so.6 /var/task/cairosvg/lib
**correct** cp /lib64/libc.so.6 /var/task/cairosvg/lib
**correct** cp /lib/ld-linux-aarch64.so.1 /var/task/cairosvg/lib
**correct** cp /lib64/libexpat.so.1 /var/task/cairosvg/lib
**correct** cp /lib64/libuuid.so.1 /var/task/cairosvg/lib
**correct** cp /var/lang/lib/libbz2.so.1 /var/task/cairosvg/lib
**correct** cp /lib64/libGLdispatch.so.0 /var/task/cairosvg/lib
**correct** cp /lib64/libXau.so.6 /var/task/cairosvg/lib
**correct** cp /lib64/libGLX.so.0 /var/task/cairosvg/lib

<!-- cp /var/task/linux-vdso.so.1 /var/task/cairosvg/lib -->
*incorrect* cp /lib/aarch64-linux-gnu/libcairo.so.2 /var/task/cairosvg/lib
*incorrect* cp /lib/aarch64-linux-gnu/libpixman-1.so.0 /var/task/cairosvg/lib
*incorrect* cp /lib/aarch64-linux-gnu/libfontconfig.so.1 /var/task/cairosvg/lib
*incorrect* cp /lib/aarch64-linux-gnu/libfreetype.so.6 /var/task/cairosvg/lib
*incorrect* cp /lib/aarch64-linux-gnu/libpng16.so.16 /var/task/cairosvg/lib
*incorrect* cp /lib/aarch64-linux-gnu/libxcb-shm.so.0 /var/task/cairosvg/lib
*incorrect* cp /lib/aarch64-linux-gnu/libxcb.so.1 /var/task/cairosvg/lib
*incorrect* cp /lib/aarch64-linux-gnu/libxcb-render.so.0 /var/task/cairosvg/lib
*incorrect* cp /lib/aarch64-linux-gnu/libXrender.so.1 /var/task/cairosvg/lib
*incorrect* cp /lib/aarch64-linux-gnu/libX11.so.6 /var/task/cairosvg/lib
*incorrect* cp /lib/aarch64-linux-gnu/libXext.so.6 /var/task/cairosvg/lib
*incorrect* cp /lib/aarch64-linux-gnu/libz.so.1 /var/task/cairosvg/lib
*incorrect* cp /lib/aarch64-linux-gnu/libm.so.6 /var/task/cairosvg/lib
*incorrect* cp /lib/aarch64-linux-gnu/libc.so.6 /var/task/cairosvg/lib
*incorrect* cp /lib/ld-linux-aarch64.so.1 /var/task/cairosvg/lib
*incorrect* cp /lib/aarch64-linux-gnu/libexpat.so.1 /var/task/cairosvg/lib
*incorrect* cp /lib/aarch64-linux-gnu/libbrotlidec.so.1 /var/task/cairosvg/lib
*incorrect* cp /lib/aarch64-linux-gnu/libXau.so.6 /var/task/cairosvg/lib
*incorrect* cp /lib/aarch64-linux-gnu/libXdmcp.so.6 /var/task/cairosvg/lib
*incorrect* cp /lib/aarch64-linux-gnu/libbrotlicommon.so.1 /var/task/cairosvg/lib
*incorrect* cp /lib/aarch64-linux-gnu/libbsd.so.0 /var/task/cairosvg/lib
*incorrect* cp /lib/aarch64-linux-gnu/libmd.so.0 /var/task/cairosvg/lib

- Test cairosvg
`touch cairosvg/python/test.py`
`cat > cairosvg/python/test.py`
- Copy the content of <test>.txt
- Press `CNTRL` + `D` (2,3 times if needed)
`python3 cairosvg/python/test.py`
- If png is created everything works.
- Delete the test
`rm cairosvg/python/test.py`

# Step 4
`cd cairosvg && zip -r cairosvg_layer.zip python lib && cd ..`
`cd python-telegram-bot && zip -r python_telegram_bot_layer.zip python && cd ..`
`cd chess && zip -r chess_layer.zip python && cd ..`

# Level 2
# Step 1
- open [AWS Lambda](https://us-east-1.console.aws.amazon.com/lambda/home?region=us-east-1)
- Click `Create function`
- Author from scratch
- Name `aws-complete-setup`
- Runtime Python 3.13
- Architecture arm64 (otherwise cairosvg will not work) **!IMPORTANT**
- Click `Create function`
- Click `Add a layer` at the bottom
- Choose `AWS layers` and AWS layers `AWSSDKPandas-Python313-Arm64`

# Step 2 (long story short)
- Then create all the layers and add them into the project
- Copy the code into the new console editor
- In the `Configuration/General configuration` Tab change `Timeout` as needed (set 1 min instead of 3 sec)

- voila