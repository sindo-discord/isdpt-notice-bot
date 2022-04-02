FROM python:3.8.3

# Your Token
ENV TOKEN=<TOKEN>
ENV USERNAME=isdpt_bot

RUN apt update
RUN pip install --upgrade pip

RUN useradd -ms /bin/bash ${USERNAME}
USER ${USERNAME}
WORKDIR /home/${USERNAME}

COPY --chown=${USERNAME}:${USERNAME} requirements.txt requirements.txt
RUN pip install --user -r requirements.txt

COPY src /home/${USERNAME}/src
COPY bot.py /home/${USERNAME}/bot.py

CMD [ "python3", "bot.py" ]
