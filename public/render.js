const startDriver = document.querySelector('#startDriver')
const stopDriver = document.querySelector('#stopDriver')
const alrtMes = document.querySelector('#alrtMes')
const additionals_wrapper = document.querySelector('.additionals_wrapper')
let driver = false
const windowURL = window.location.href
const additionalButtonList = document.querySelectorAll('.additionalButton')
const contentWrapper = document.querySelector('.content')
const mainBlock = document.querySelector('main')
const save_account_button = document.querySelector('#save_account_data')


// Загрузка значений из data.json в inputs
function loadAdditionalsData(data) {
    for (const key in data) {
        const element = additionals_wrapper.querySelector(`input[name="${key}"]`)
        if (!element) {
            continue
        }
        if (element.type == 'checkbox') {
            element.checked = data[key] === 'true'
        } else {
            element.value = data[key]
        }
    }
}
eel.getJson()().then(json_data_obj => {
    loadAdditionalsData(json_data_obj)
})
// Additional blocks
save_account_button.addEventListener('click', () => {
    const wrapper = save_account_button.parentElement
    const inputs = wrapper.querySelectorAll('input')

    data = {}

    inputs.forEach(e => {
        if (e.type == 'checkbox') {
            if (e.checked) {
                data[e.name] = 'true'
            } else {
                data[e.name] = 'false'
            }
        } else {
            data[e.name] = e.value
        }
    });

    console.log(data);
    eel.writeJson(data)()
})


eel.expose(alertMessage);
function alertMessage(message, mode) {
    alrtMes.classList.remove('red', 'green')
    alrtMes.classList.add('active', mode)
    alrtMes.innerHTML = message

    setTimeout(() => {
        alrtMes.classList.remove('active')
    }, 2000);
}

// Start/Stop driver
startDriver.addEventListener('click', async () => {
    driver = await eel.createDriver()()
    eel.start()
    if(driver) {
        alertMessage('webdriver started', 'green')
    }
})
stopDriver.addEventListener('click', async () => {
    if(!driver) {
        alertMessage('webdriver already quited')
        return
    }
    driver = await eel.quit()()
    if(!driver) {
        alertMessage('webdriver quit', 'green')
    }
})


function addChatMessage(role, content) {
    const wrapper = document.createElement('div')
    wrapper.classList.add('chat_block')

    const avatar = document.createElement('div')
    avatar.classList.add('avatare_circle', 'mr-right-10')
    if (role == 'chatGPT') {
        avatar.style.backgroundColor = 'green'
    } else if (role == 'You') {
        avatar.style.backgroundColor = 'brown'
    }

    const chat_right = document.createElement('div')
    chat_right.classList.add('chat_right')

    const title = document.createElement('span')
    title.classList.add('title2')
    title.innerHTML = role
    const title_block = document.createElement('div')
    title_block.appendChild(title)

    const content_block = document.createElement('div')
    content_block.classList.add('p_text', 'mr-top-10')
    content_block.innerHTML = content

    chat_right.appendChild(title_block)
    chat_right.appendChild(content_block)
    wrapper.appendChild(avatar)
    wrapper.appendChild(chat_right)

    contentWrapper.appendChild(wrapper)
    mainBlock.scrollTop = mainBlock.scrollHeight
}

const sendPrompt = document.querySelector('#sendPrompt')
sendPrompt.addEventListener('click', async () => {
    const promptArea = document.querySelector('#inputPrompt')
    const content = promptArea.value
    if(content.lenght == 0) {
        console.log('empty prompt')
        return
    }
    if(!driver) {
        console.log('driver not found')
        return
    }
    eel.sendPrompt(JSON.stringify({data: content}))()
    addChatMessage('You', content)
})

eel.expose(close_window);
function close_window() {
    window.close()
}
eel.expose(open_window);
function open_window() {
    window.open(windowURL, "_blank", "width=800,height=500");
}


// Вставка html
eel.expose(insertAnswear);
function insertAnswear(htmlText) {
    addChatMessage('chatGPT', htmlText)
}

// автоматическое закрытие webdriver
window.onbeforeunload = function() {
    eel.quit()
};


















