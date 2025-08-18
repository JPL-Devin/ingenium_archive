FROM cae-artifactory.jpl.nasa.gov:17001/node:16.17.0
WORKDIR /app
COPY . /app
RUN npm ci
USER node
ENTRYPOINT ["node", "index.js"]
