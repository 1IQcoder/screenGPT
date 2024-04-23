const { app, BrowserWindow, ipcMain, globalShortcut } = require('electron')
const url = require('url')
const fs = require('fs')
const path = require('path')

let win = null

function CreateMainWindow() {
    win = new BrowserWindow({
        width: 600, height: 538, icon: __dirname + '/img/icon.png',
        webPreferences: {
            nodeIntegration: true,
            preload: path.join(__dirname, 'preload.js')
        },
        // resizable: false,
    })
    win.setMenu(null);
    
    win.loadURL(url.format({
        pathname: __dirname + '/public/index.html',
        protocol: 'file:',
        slashes: true
    }))
}

app.on('ready', CreateMainWindow)

app.on('window-all-closed', () => {
    globalShortcut.unregisterAll();
    app.quit()
})