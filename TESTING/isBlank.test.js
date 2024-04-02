

const isBlank = require('./isBlank')

test('Tests if user input is blank, if so return true', () => {
    var input = "";
    
    expect(isBlank(input)).toBe(true)
    
})

test('Tests if user input is blank, if not return true', () => {
    var input = "notblank";
    
    expect(isBlank(input)).toBe(false)
    
})