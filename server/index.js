const http = require('http')
const {WebSocketServer} = require('ws')

const server = http.createServer()
const wsServer = new WebSocketServer({server})
const port = 5173

server.listen(port, () => {
    console.log(`Websocket server is running on port ${port}`)
})