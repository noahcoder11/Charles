const charlesConfigLoadable = new Loadable();


let audioConfigHasChanges = false

//Define the audio select boxes (to get values from later)
const inputDeviceSelect = select({ classes: ['uk-select'], content: [], eventListeners: {
    change: () => {
        audioConfigHasChanges = true
        saveButton.removeAttribute('disabled')
    }
} })
const outputDeviceSelect = select({ classes: ['uk-select'], content: [], eventListeners: {
    change: () => {
        audioConfigHasChanges = true
        saveButton.removeAttribute('disabled')
    }
} })


//Define the test button
const testAudioLoadable = new Loadable('existing')
const testAudio = async (device_index) => await postRequest('/test-audio', { device_index: device_index })
const testButton = button({ classes: ['uk-button', 'uk-button-primary'], style: { marginLeft: '10px' }, content: 'Test', 
    eventListeners: { click: (e) => {
        e.preventDefault()
        console.log('Testing audio')
        console.log(outputDeviceSelect)
        let outputDevice = parseInt(outputDeviceSelect.value)
        console.log('Output device:', outputDevice)
        //Request a test audio 
        testAudioLoadable.loadWithPromise(async () => testAudio(outputDevice))
    } } 
})
attachToLoadable(testButton, testAudioLoadable, {
    onLoading: (element) => element.innerHTML = centeredSpinner(),
    onError: (element, error) => element.innerHTML = `Test`,
    onData: (element, data) => element.innerHTML = `Test`
})

const saveAudioLoadable = new Loadable('existing')
const saveButton = button({ classes: ['uk-button', 'uk-button-primary'], content: 'Save Changes', style: { marginTop: '10px' }, eventListeners: {
    click: (e) => {
        e.preventDefault()
        if (audioConfigHasChanges) {
            let inputDevice = parseInt(inputDeviceSelect.value)
            let outputDevice = parseInt(outputDeviceSelect.value)

            console.log(inputDevice)

            //Request an audio test
            saveAudioLoadable.loadWithPromise(async () => saveAudio({ input_device_index: inputDevice, output_device_index: outputDevice }))
        }
    }
}})
const saveAudio = async (config) => await postRequest('/config', config)
attachToLoadable(saveButton, saveAudioLoadable, {
    onLoading: (element) => element.innerHTML = centeredSpinner(),
    onError: (element, error) => element.innerHTML = `Save Changes`,
    onData: (element, data) => {
        audioConfigHasChanges = false
        element.setAttribute('disabled', true)
        element.innerHTML = `Save Changes`
    }
})


attachToLoadable('audio-config', charlesConfigLoadable, {
    onLoading: (element) => element.innerHTML = centeredSpinner(),
    onError: (element, error) => element.innerHTML = `<p>Error: ${error}</p>`,
    onData: (element, data) => {
        const deviceOptions = data.available_devices.map((device, index) => `<option value='${index}'>#${index} - ${device.name} (${device.max_input_channels}:${device.max_output_channels})</option>`).join('\n')
        
        outputDeviceSelect.innerHTML = deviceOptions
        inputDeviceSelect.innerHTML = deviceOptions

        outputDeviceSelect.value = data.output_device_index || 0
        inputDeviceSelect.value = data.input_device_index || 0
        
        const newContent = [
            div({ classes: ['form-item'], content: [
                label({ classes: ['uk-form-label'], content: 'Input Device' }),
                inputDeviceSelect
            ] }),
            div({ classes: ['form-item'], content: [
                label({ classes: ['uk-form-label'], content: 'Output Device' }),
                div({ classes: ['uk-form-controls'], style: {
                    display: 'flex',
                    flexDirection: 'row',
                    justifyContent: 'space-between'
                }, content: [
                    outputDeviceSelect,
                    testButton
                ] })
            ] }),
            saveButton.withAttribute('disabled', !audioConfigHasChanges)
        ]

        element.setChildren(newContent)

    }
})

attachToLoadable('server-config', charlesConfigLoadable, {
    onLoading: (element) => element.innerHTML = centeredSpinner(),
    onError: (element, error) => element.innerHTML = `<p>Error: ${error}</p>`,
    onData: (element, data) => {
        const newContent = [
            div({ classes: ['form-item'], content: [
                label({ classes: ['uk-form-label'], content: 'URL' }),
                input({ classes: ['uk-input'], attributes: { value: data.server_url, disabled: true } })
            ] })
        ]
        
        element.setChildren(newContent)
    }
})

charlesConfigLoadable.loadWithPromise(async () => {
    console.log('Fetching audio config')
    const response = await fetch('/config')
    return response.json()
})







const charlesLogsLoadable = new Loadable()
attachToLoadable('log-viewer', charlesLogsLoadable, {
    onLoading: (element) => element.innerHTML = centeredSpinner(),
    onError: (element, error) => element.innerHTML = `<p>Error: ${error}</p>`,
    onData: (element, data) => {
        const currentLogEntries = document.getElementById('log-viewer').getElementsByClassName('charles-log-entries')
        
        const newLogEntries = data.logs.split('\\n')

        let startingIndex = 0
        if (currentLogEntries.length > 0) {
            startingIndex = newLogEntries.findIndex((entry, index) => entry !== currentLogEntries[index].innerHTML)
        }

        const entriesToAdd = newLogEntries.slice(startingIndex)

        const newContent = [ 
            div({ classes: ['uk-card', 'uk-card-secondary'], style: { boxShadow: 'none', border: 'none', marginTop: '0px' }, content: [
                logViewerElement
            ]
            }) ] 

        for (let i = startingIndex; i < currentLogEntries.length; i++) {
            const entry = currentLogEntries[i]
            entry.remove()
        }

        for (let i = 0; i < entriesToAdd.length; i++) {
            const entry = entriesToAdd[i]
            logViewerElement.appendChild(pre({ classes: ['uk-text-left'], content: entry }))
        }

        if (!element.contains(logViewerElement)) {
            element.setChildren(newContent)
        }
    }
})

const logViewerElement = div({ classes: ['uk-card-body', 'charles-log-entry'], style: { overflowX: 'scroll' }, content: []})
charlesLogsLoadable.loadWithPromise(async () => {
    console.log('Fetching logs')
    return await getRequest('/logs')
})

window.setInterval(() => {
    charlesLogsLoadable.silentlyLoadWithPromise(async () => {
        console.log('Fetching logs')
        return await getRequest('/logs')
    })
}, 3000)


const clearLogsLoadable = new Loadable('existing')
const _clearLogs = async () => await postRequest('/clear-logs')
const clearLogs = () => {
    console.log('Clearing')
    clearLogsLoadable.loadWithPromise(_clearLogs)
} 
attachToLoadable('clear-logs', clearLogsLoadable, {
    onLoading: (element) => element.innerHTML = centeredSpinner(),
    onError: (element, error) => element.innerHTML = `Clear Logs`,
    onData: (element, data) => element.innerHTML = `Clear Logs`
})
