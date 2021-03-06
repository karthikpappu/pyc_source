# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/lib/python2.5/site-packages/pyjamas/DOM.py
# Compiled at: 2008-09-04 14:59:46
__doc__ = '\n    DOM implements the core of Pjamas-Desktop, providing access to\n    and management of the DOM model of the PyWebkitGtk window.\n'
from Window import onResize, onClosing, onClosed
from pyjamas.__pyjamas__ import JS, doc, get_main_frame, wnd
sCaptureElem = None
sEventPreviewStack = []

def _dispatchEvent(evt):
    listener = None
    curElem = evt.props.target
    while curElem and not hasattr(curElem, '_listener'):
        curElem = getParent(curElem)

    if curElem and getNodeType(curElem) != 1:
        curElem = None
    if curElem and hasattr(curElem, '_listener') and curElem._listener:
        dispatchEvent(evt, curElem, curElem._listener)
    return


def _dispatchCapturedMouseEvent(evt):
    if _dispatchCapturedEvent(evt):
        mf = get_main_frame()
        cap = mf._captureElem
        if cap and cap._listener:
            dispatchEvent(evt, cap, cap._listener)
            evt.stop_propagation()


def _dispatchCapturedMouseoutEvent(evt):
    mf = get_main_frame()
    cap = mf._captureElem
    if cap:
        print 'cap', dir(evt), cap
        if not eventGetToElement(evt):
            print 'synthesise', cap
            mf._captureElem = None
            if cap._listener:
                lcEvent = doc().create_event('UIEvent')
                lcEvent.init_ui_event('losecapture', False, False, wnd(), 0)
                dispatchEvent(lcEvent, cap, cap._listener)
    return


def browser_event_cb(view, event, from_window):
    et = eventGetType(event)
    if et == 'resize':
        onResize()
        return
    elif et == 'mouseout':
        print 'mouse out', event
        _dispatchCapturedMouseoutEvent(event)
    elif et == 'keyup' or et == 'keydown' or et == 'keypress' or et == 'change':
        _dispatchCapturedEvent(event)
    else:
        _dispatchCapturedMouseEvent(event)


def _dispatchCapturedEvent(event):
    if not previewEvent(event):
        event.stop_propagation()
        event.prevent_default()
        return False
    return True


def init():
    mf = get_main_frame()
    mf._captureElem = None
    mf.connect('browser-event', browser_event_cb)
    mf.add_window_event_listener('click')
    mf.add_window_event_listener('change')
    mf.add_window_event_listener('mouseout')
    mf.add_window_event_listener('mousedown')
    mf.add_window_event_listener('mouseup')
    mf.add_window_event_listener('resize')
    mf.add_window_event_listener('keyup')
    mf.add_window_event_listener('keydown')
    mf.add_window_event_listener('keypress')
    return


def old_javascript_based_init():
    print 'TODO'
    return
    JS("\n    // Set up capture event dispatchers.\n    $wnd.__dispatchCapturedMouseEvent = function(evt) {\n        if ($wnd.__dispatchCapturedEvent(evt)) {\n            var cap = $wnd._captureElem;\n            if (cap && cap._listener) {\n                DOM_dispatchEvent(evt, cap, cap._listener);\n                evt.stopPropagation();\n            }\n        }\n    };\n\n    $wnd.__dispatchCapturedEvent = function(evt) {\n        if (!DOM_previewEvent(evt)) {\n            evt.stopPropagation();\n            evt.preventDefault();\n            return false;\n        }\n\n        return true;\n        };\n\n    $wnd.addEventListener(\n        'mouseout',\n        function(evt){\n            var cap = $wnd._captureElem;\n            if (cap) {\n                if (!evt.relatedTarget) {\n                    // When the mouse leaves the window during capture, release capture\n                    // and synthesize an 'onlosecapture' event.\n                    $wnd._captureElem = null;\n                    if (cap._listener) {\n                        var lcEvent = $doc.createEvent('UIEvent');\n                        lcEvent.initUIEvent('losecapture', false, false, $wnd, 0);\n                        DOM_dispatchEvent(lcEvent, cap, cap._listener);\n                    }\n                }\n            }\n        },\n        true\n    );\n\n\n    $wnd.addEventListener('click', $wnd.__dispatchCapturedMouseEvent, true);\n    $wnd.addEventListener('dblclick', $wnd.__dispatchCapturedMouseEvent, true);\n    $wnd.addEventListener('mousedown', $wnd.__dispatchCapturedMouseEvent, true);\n    $wnd.addEventListener('mouseup', $wnd.__dispatchCapturedMouseEvent, true);\n    $wnd.addEventListener('mousemove', $wnd.__dispatchCapturedMouseEvent, true);\n    $wnd.addEventListener('keydown', $wnd.__dispatchCapturedEvent, true);\n    $wnd.addEventListener('keyup', $wnd.__dispatchCapturedEvent, true);\n    $wnd.addEventListener('keypress', $wnd.__dispatchCapturedEvent, true);\n    \n    $wnd.__dispatchEvent = function(evt) {\n    \n        var listener, curElem = this;\n        \n        while (curElem && !(listener = curElem._listener)) {\n            curElem = curElem.props.parent_node;\n        }\n        if (curElem && curElem.props.node_type != 1) {\n            curElem = null;\n        }\n    \n        if (listener) {\n            DOM_dispatchEvent(evt, curElem, listener);\n        }\n    };\n    \n    $wnd._captureElem = null;\n    ")


def addEventPreview(preview):
    global sEventPreviewStack
    sEventPreviewStack.append(preview)


def appendChild(parent, child):
    print 'appendChild', parent, child
    parent.append_child(child)


def compare(elem1, elem2):
    return elem1.is_same_node(elem2)


def createAnchor():
    return createElement('A')


def createButton():
    return createElement('button')


def createCol():
    return createElement('col')


def createDiv():
    return createElement('div')


def createElement(tag):
    return doc().create_element(tag)


def createFieldSet():
    return createElement('fieldset')


def createForm():
    return createElement('form')


def createIFrame():
    return createElement('iframe')


def createImg():
    return createElement('img')


def createInputCheck():
    return createInputElement('checkbox')


def createInputElement(elementType):
    e = createElement('INPUT')
    e.props.type = elementType
    return e


def createInputPassword():
    return createInputElement('password')


def createInputRadio(group):
    e = createInputElement('radio')
    e.props.name = group
    return e


def createInputText():
    return createInputElement('text')


def createLabel():
    return createElement('label')


def createLegend():
    return createElement('legend')


def createOptions():
    return createElement('options')


def createSelect():
    return createElement('select')


def createSpan():
    return createElement('span')


def createTable():
    return createElement('table')


def createTBody():
    return createElement('tbody')


def createTD():
    return createElement('td')


def createTextArea():
    return createElement('textarea')


def createTH():
    return createElement('th')


def createTR():
    return createElement('tr')


def eventCancelBubble(evt, cancel):
    evt.cancelBubble = cancel


def eventGetAltKey(evt):
    return evt.props.alt_key


def eventGetButton(evt):
    return evt.props.button


def eventGetClientX(evt):
    return evt.props.client_x


def eventGetClientY(evt):
    return evt.props.client_y


def eventGetCtrlKey(evt):
    return evt.props.ctrl_key


def eventGetFromElement(evt):
    return evt.props.from_element


def eventGetKeyCode(evt):
    return evt.props.which and evt.props.key_code


def eventGetRepeat(evt):
    return evt.props.repeat


def eventGetScreenX(evt):
    return evt.props.screen_x


def eventGetScreenY(evt):
    return evt.props.screen_y


def eventGetShiftKey(evt):
    return evt.props.shift_key


def eventGetTarget(event):
    return event.props.target


def eventGetToElement(evt):
    return evt.props.related_target
    JS('\n    return evt.relatedTarget ? evt.relatedTarget : null;\n    ')


def eventGetType(event):
    return event.props.type


def eventGetTypeInt(event):
    JS('\n    switch (event.type) {\n      case "blur": return 0x01000;\n      case "change": return 0x00400;\n      case "click": return 0x00001;\n      case "dblclick": return 0x00002;\n      case "focus": return 0x00800;\n      case "keydown": return 0x00080;\n      case "keypress": return 0x00100;\n      case "keyup": return 0x00200;\n      case "load": return 0x08000;\n      case "losecapture": return 0x02000;\n      case "mousedown": return 0x00004;\n      case "mousemove": return 0x00040;\n      case "mouseout": return 0x00020;\n      case "mouseover": return 0x00010;\n      case "mouseup": return 0x00008;\n      case "scroll": return 0x04000;\n      case "error": return 0x10000;\n    }\n    ')


def eventGetTypeString(event):
    return eventGetType(event)


def eventPreventDefault(evt):
    evt.prevent_default()


def eventSetKeyCode(evt, key):
    evt.props.key_code = key


def eventToString(evt):
    return evt.to_strign


def iframeGetSrc(elem):
    return elem.props.src


def getAbsoluteLeft(elem):
    left = 0
    while elem:
        left += elem.props.offset_left - elem.props.scroll_left
        parent = elem.props.offset_parent
        if parent and parent.props.tag_name == 'BODY' and hasattr(elem, 'style') and getStyleAttribute(elem, 'position') == 'absolute':
            break
        elem = parent

    return left + doc().props.body.props.scroll_left


def getAbsoluteTop(elem):
    top = 0
    while elem:
        top += elem.props.offset_top - elem.props.scroll_top
        parent = elem.props.offset_parent
        if parent and parent.props.tag_name == 'BODY' and hasattr(elem, 'style') and getStyleAttribute(elem, 'position') == 'absolute':
            break
        elem = parent

    return top + doc().props.body.props.scroll_top


def getAttribute(elem, attr):
    return str(elem.get_property(mash_name_for_glib(attr)))


def getElemAttribute(elem, attr):
    if not elem.has_attribute(attr):
        return str(elem.get_property(mash_name_for_glib(attr)))
    return str(elem.get_attribute(attr))


def getBooleanAttribute(elem, attr):
    return bool(elem.get_property(mash_name_for_glib(attr)))


def getBooleanElemAttribute(elem, attr):
    if not elem.has_attribute(attr):
        return
    return bool(elem.get_attribute(attr))


def getCaptureElement():
    global sCaptureElem
    return sCaptureElem


def getChild(elem, index):
    """
    Get a child of the DOM element by specifying an index.
    """
    count = 0
    child = elem.props.first_child
    while child:
        next = child.props.next_sibling
        if child.props.node_type == 1:
            if index == count:
                return child
            count += 1
        child = next

    return


def getChildCount(elem):
    """
    Calculate the number of children the given element has.  This loops
    over all the children of that element and counts them.
    """
    count = 0
    child = elem.props.first_child
    while child:
        if child.props.node_type == 1:
            count += 1
        child = child.props.next_sibling

    return count


def getChildIndex(parent, toFind):
    """
    Return the index of the given child in the given parent.
    
    This performs a linear search.
    """
    count = 0
    child = parent.props.first_child
    while child:
        if child == toFind:
            return count
        if child.props.node_type == 1:
            count += 1
        child = child.props.next_sibling

    return -1


def getElementById(id):
    """
    Return the element in the document's DOM tree with the given id.
    """
    return doc().get_element_by_id(id)


def getEventListener(element):
    """
    See setEventListener for more information.
    """
    return element._listener


def getEventsSunk(element):
    print 'TODO'
    return 0
    JS('\n    return element.__eventBits ? element.__eventBits : 0;\n    ')


def getFirstChild(elem):
    child = elem and elem.props.first_child
    while child and child.props.node_type != 1:
        child = child.props.next_sibling

    return child


def getInnerHTML(element):
    return element and element.props.inner_html


def getInnerText(element):
    text = ''
    child = element.props.first_child
    while child:
        if child.props.node_type == 1:
            text += child.get_inner_text()
        elif child.props.node_value:
            text += child.props.node_value
        child = child.props.next_sibling

    return text


def getIntAttribute(elem, attr):
    return int(elem.get_property(mash_name_for_glib(attr)))


def getIntElemAttribute(elem, attr):
    if not elem.has_attribute(attr):
        return
    return int(elem.get_attribute(attr))


def getIntStyleAttribute(elem, attr):
    return int(elem.style.get_property(mash_name_for_glib(attr)))


def getNextSibling(elem):
    sib = elem.props.next_sibling
    while sib and sib.props.node_type != 1:
        sib = sib.props.next_sibling

    return sib


def getNodeType(elem):
    return elem.props.node_type


def getParent(elem):
    parent = elem.props.parent_node
    if parent is None:
        return
    if getNodeType(parent) != 1:
        return
    return parent


def getStyleAttribute(elem, attr):
    return elem.style.get_property(mash_name_for_glib(attr))


def insertChild(parent, toAdd, index):
    count = 0
    child = parent.props.first_child
    before = None
    while child:
        if child.props.node_type == 1:
            if count == index:
                before = child
                break
            count += 1
        child = child.props.next_sibling

    if before is None:
        parent.append_child(toAdd)
    else:
        parent.insert_before(toAdd, before)
    return


def iterChildren(elem):
    """
    Returns an iterator over all the children of the given
    DOM node.
    """
    JS("\n    var parent = elem;\n    var child = elem.props.first_child;\n    var lastChild = null;\n    return {\n        'next': function() {\n            if (child == null) {\n                throw StopIteration;\n            }\n            lastChild = child;\n            child = DOM_getNextSibling(child);\n            return lastChild;\n        },\n        'remove': function() {        \n            parent.removeChild(lastChild);\n        },\n        __iter__: function() {\n            return this;\n        }\n    };\n    ")


def walkChildren(elem):
    """
    Walk an entire subtree of the DOM.  This returns an
    iterator/iterable which performs a pre-order traversal
    of all the children of the given element.
    """
    JS("\n    var parent = elem;\n    var child = DOM_getFirstChild(elem);\n    var lastChild = null;\n    var stack = [];\n    var parentStack = [];\n    return {\n        'next': function() {\n            if (child == null) {\n                throw StopIteration;\n            }\n            lastChild = child;\n            var props.first_child = DOM_getFirstChild(child);\n            var props.next_sibling = DOM_getNextSibling(child);\n            if(props.first_child != null) {\n               if(props.next_sibling != null) {\n                   stack.push(props.next_sibling);\n                   parentStack.push(parent);\n                }\n                parent = child;\n                child = props.first_child;\n            } else if(props.next_sibling != null) {\n                child = props.next_sibling;\n            } else if(stack.length > 0) {\n                child = stack.pop();\n                parent = parentStack.pop();\n            } else {\n                child = null;\n            }\n            return lastChild;\n        },\n        'remove': function() {        \n            parent.removeChild(lastChild);\n        },\n        __iter__: function() {\n            return this;\n        }\n    };\n    ")


def isOrHasChild(parent, child):
    while child:
        if parent == child:
            return True
        child = child.props.parent_node
        if not child:
            return False
        if child.props.node_type != 1:
            child = None

    return False


def releaseCapture(elem):
    global sCaptureElem
    if sCaptureElem and compare(elem, sCaptureElem):
        sCaptureElem = None
    return
    JS('\n    if ((DOM_sCaptureElem != null) && DOM_compare(elem, DOM_sCaptureElem))\n        DOM_sCaptureElem = null;\n\n    if (elem == $wnd._captureElem)\n        $wnd._captureElem = null;\n    ')


def removeChild(parent, child):
    parent.remove_child(child)


def replaceChild(parent, newChild, oldChild):
    parent.replace_child(newChild, oldChild)


def removeEventPreview(preview):
    sEventPreviewStack.remove(preview)


def scrollIntoView(elem):
    left = elem.props.offset_left
    top = elem.props.offset_top
    width = elem.props.offset_width
    height = elem.props.offset_height
    if elem.props.parent_node != elem.props.offset_parent:
        left -= elem.props.parent_node.props.offset_left
        top -= elem.props.parent_node.props.offset_top
    cur = elem.props.parent_node
    while cur and cur.props.node_type == 1:
        if hasattr(cur, 'style') and (cur.style.overflow == 'auto' or cur.style.overflow == 'scroll'):
            if left < cur.props.scroll_left:
                cur.props.scroll_left = left
            if left + width > cur.props.scroll_left + cur.props.client_width:
                cur.props.scroll_left = left + width - cur.props.client_width
            if top < cur.props.scroll_top:
                cur.props.scroll_top = top
            if top + height > cur.props.scroll_top + cur.props.client_height:
                cur.props.scroll_top = top + height - cur.props.client_height
        offset_left = cur.props.offset_left
        offset_top = cur.props.offset_top
        if cur.props.parent_node != cur.props.offset_parent:
            if hasattr(cur.props.parent_node.props, 'offset_left'):
                offset_left -= cur.props.parent_node.props.offset_left
            if hasattr(cur.props.parent_node.props, 'offset_top'):
                offset_top -= cur.props.parent_node.props.offset_top
        left += offset_left - cur.props.scroll_left
        top += offset_top - cur.props.scroll_top
        cur = cur.props.parent_node


def mash_name_for_glib(name, joiner='-'):
    res = ''
    for c in name:
        if c.isupper():
            res += joiner + c.lower()
        else:
            res += c

    return res


def removeAttribute(element, attribute):
    elem.remove_attribute(attribute)


def setAttribute(element, attribute, value):
    element.set_property(mash_name_for_glib(attribute), value)


def setElemAttribute(element, attribute, value):
    element.set_attribute(attribute, value)


def setBooleanAttribute(elem, attr, value):
    elem.set_property(mash_name_for_glib(attr), value)


def setCapture(elem):
    global sCaptureElem
    sCaptureElem = elem
    mf = get_main_frame()
    mf._captureElem = elem
    return
    JS('\n    DOM_sCaptureElem = elem;\n    $wnd._captureElem = elem;\n    ')


def setEventListener(element, listener):
    """
    Register an object to receive event notifications for the given
    element.  The listener's onBrowserEvent() method will be called
    when a captured event occurs.  To set which events are captured,
    use sinkEvents().
    """
    element._listener = listener


def setInnerHTML(element, html):
    element.props.inner_html = html


def setInnerText(elem, text):
    while elem.props.first_child:
        elem.remove_child(elem.props.first_child)

    elem.append_child(doc().create_text_node(text or ''))


def setIntElemAttribute(elem, attr, value):
    elem.set_attribute(attr, str(value))


def setIntAttribute(elem, attr, value):
    elem.set_property(mash_name_for_glib(attr), value)


def setIntStyleAttribute(elem, attr, value):
    sty = elem.props.style
    sty.set_css_property(mash_name_for_glib(attr), str(value), '')


def setOptionText(select, text, index):
    print 'TODO - setOptionText'
    JS('\n    var option = select.options[index];\n    option.text = text;\n    ')


def setStyleAttribute(element, name, value):
    sty = element.props.style
    sty.set_css_property(mash_name_for_glib(name), value, '')


def dispatch_event_cb(element, event, capture):
    print 'dispatch_event_cb', element, event, capture


def sinkEvents(element, bits):
    """
    Set which events should be captured on a given element and passed to the
    registered listener.  To set the listener, use setEventListener().
    
    @param bits: A combination of bits; see ui.Event for bit values
    """
    element.__eventBits = bits
    if bits:
        element.connect('browser-event', lambda x, y, z: _dispatchEvent(y))
    if bits & 1:
        element.add_event_listener('click', True)
    if bits & 2:
        element.add_event_listener('dblclick', True)
    if bits & 4:
        element.add_event_listener('mousedown', True)
    if bits & 8:
        element.add_event_listener('mouseup', True)
    if bits & 16:
        element.add_event_listener('mouseover', True)
    if bits & 32:
        element.add_event_listener('mouseout', True)
    if bits & 64:
        element.add_event_listener('mousemove', True)
    if bits & 128:
        element.add_event_listener('keydown', True)
    if bits & 256:
        element.add_event_listener('keypress', True)
    if bits & 512:
        element.add_event_listener('keyup', True)
    if bits & 1024:
        element.add_event_listener('change', True)
    if bits & 2048:
        element.add_event_listener('focus', True)
    if bits & 4096:
        element.add_event_listener('blur', True)
    if bits & 8192:
        element.add_event_listener('losecapture', True)
    if bits & 16384:
        element.add_event_listener('scroll', True)
    if bits & 32768:
        element.add_event_listener('load', True)
    if bits & 65536:
        element.add_event_listener('error', True)


def toString(elem):
    temp = elem.clone_node(True)
    tempDiv = createDiv()
    tempDiv.append_child(temp)
    outer = tempDiv.props.inner_html
    temp.props.inner_html = ''
    return outer


def dispatchEvent(event, element, listener):
    dispatchEventImpl(event, element, listener)


def previewEvent(evt):
    ret = True
    if len(sEventPreviewStack) > 0:
        preview = sEventPreviewStack[(len(sEventPreviewStack) - 1)]
        ret = preview.onEventPreview(evt)
        if not ret:
            eventCancelBubble(evt, True)
            eventPreventDefault(evt)
    return ret


def dispatchEventAndCatch(evt, elem, listener, handler):
    pass


def dispatchEventImpl(event, element, listener):
    global sCaptureElem
    if element == sCaptureElem:
        if eventGetType(event) == 'losecapture':
            sCaptureElem = None
    listener.onBrowserEvent(event)
    return


def insertListItem(select, item, value, index):
    option = createElement('OPTION')
    setInnerText(option, item)
    if value != None:
        setAttribute(option, 'value', value)
    if index == -1:
        appendChild(select, option)
    else:
        insertChild(select, option, index)
    return