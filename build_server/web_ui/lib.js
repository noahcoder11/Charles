const LoadableState = {
    NOT_STARTED: 'notStarted',
    LOADING: 'loading',
    ERROR: 'error',
    DATA: 'data',
    DONE: 'done' // Optional, usually for marking the end of a paginated list of loads
  };
  
  class LoadableUpdate {
    constructor(state, { error = null, data = null } = {}) {
      this.state = state;
      this.error = error;
      this.data = data;
    }
  }
  
  class Loadable {
    constructor(initialValue = null) {
      this._currentPromise = null;
      this._value = initialValue;
      this._listeners = [];
    }
  
    get value() {
      return this._value;
    }
  
    set value(newValue) {
      this._value = newValue;
      if (newValue !== null) {
        this._notifyListeners(new LoadableUpdate(LoadableState.DATA, { data: this._value }));
      }
    }
  
    async reload() {
      if (this._currentPromise) {
        await this.loadWithPromise(this._currentPromise);
      }
    }
  
    async loadWithPromise(promiseFactory) {
      this._currentPromise = promiseFactory;
  
      // Start loading
      this._notifyListeners(new LoadableUpdate(LoadableState.LOADING));
  
      try {
        // Load the data
        this._value = await promiseFactory();
        // Update the stream
        if (this._value !== null) {
          this._notifyListeners(new LoadableUpdate(LoadableState.DATA, { data: this._value }));
        }
      } catch (error) {
        this._notifyListeners(new LoadableUpdate(LoadableState.ERROR, { error: error.toString() }));
        throw error;
      }
  
      return this._value;
    }
  
    async silentlyLoadWithPromise(promiseFactory) {
      this._currentPromise = promiseFactory;
  
      try {
        // Load the data
        this._value = await promiseFactory();
        // Update the stream
        if (this._value !== null) {
          this._notifyListeners(new LoadableUpdate(LoadableState.DATA, { data: this._value }));
        }
      } catch (error) {
        this._notifyListeners(new LoadableUpdate(LoadableState.ERROR, { error: error.toString() }));
        throw error;
      }
  
      return this._value;
    }
  
    _notifyListeners(update) {
      this._listeners.forEach(listener => listener(update));
    }
  
    listenToStream(onData) {
      this._listeners.push(onData);
      return {
        unsubscribe: () => {
          this._listeners = this._listeners.filter(listener => listener !== onData);
        }
      };
    }
  
    dispose() {
      this._listeners = [];
    }
  }
  
  // Example usage:
  // const loadable = new Loadable();
  // loadable.listenToStream(update => console.log(update));
  // loadable.loadWithPromise(() => fetch('/data').then(response => response.json()));

function attachToLoadable(elementId, loadable, { onLoading, onError, onData } = {}) {

    const element = (typeof elementId == 'string' ? document.getElementById(elementId):elementId);

    const updateElement = update => {
        switch (update.state) {
            case LoadableState.NOT_STARTED:
                if (loadable.value) onData(element, loadable.value)
                else onLoading(element)
                break;
            case LoadableState.LOADING:
                onLoading(element)
                break;
            case LoadableState.ERROR:
                onError(element, update.error)
                break;
            case LoadableState.DATA:
                onData(element, update.data)
                break;
            default:
            throw new Error(`Invalid state: ${update.state}`);
        }
    }
  
    const subscription = loadable.listenToStream(updateElement);
  
    updateElement(new LoadableUpdate(LoadableState.NOT_STARTED));

    return {
        unsubscribe: subscription.unsubscribe
    }
}

Node.prototype.getHTML = function() {
    var wrap = document.createElement("div");
    var cthis = this.clone();
    wrap.appendChild(cthis);
    return wrap.innerHTML;
}

Node.prototype.setChildren = function(children) {
    this.innerHTML = '';
    children.forEach(child => this.appendChild(child));
}
Node.prototype.withAttribute = function(name, value) {
    this.setAttribute(name, value);
    return this;
}

//Components
const centeredSpinner = (ratio=1) => `<div uk-spinner="ratio: ${0.5}" style="display: flex; flex-direction: row; align-items: center; justify-content: center;"></div>`;
const htmlComponent = (elementName, { id, classes, eventListeners, attributes, style, content }) => {
    const element = document.createElement(elementName)
    if (id) element.id = id
    if (classes) element.classList.add(...classes)
    if (eventListeners) Object.entries(eventListeners).forEach(([event, listener]) => element.addEventListener(event, listener))
    if (attributes) Object.entries(attributes).forEach(([key, value]) => element.setAttribute(key, value))
    if (style) Object.entries(style).forEach(([key, value]) => element.style[key] = value)
    if (content) {
        if (typeof content === 'string') {
            element.innerHTML = content
        } else {
            content.forEach(child => element.appendChild(child))
        }
    }
    return element
}
const div = (options) => htmlComponent('div', options)
const button = (options) => htmlComponent('button', options)
const label = (options) => htmlComponent('label', options)
const select = (options) => htmlComponent('select', options)
const option = (options) => htmlComponent('option', options)
const input = (options) => htmlComponent('input', options)
const pre = (options) => htmlComponent('pre', options)
const h3 = (options) => htmlComponent('h3', options)



async function postRequest(url, data) {
    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    return response.json()
}

async function getRequest(url) {
    const response = await fetch(url)
    return response.json()
}