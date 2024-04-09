const checkPasswordMatch = require('./checkPasswordMatch')

test('Tests if passwords match, if so return true', () => {

    var input = "password";
    
    expect(checkPasswordMatch(input)).toBe(true)
    
})

test('Tests if passwords do not match, if so return false', () => {

    var input = "123";
    
    expect(checkPasswordMatch(input)).toBe(false)
    
})

test('Tests if passwords do not match, case-sensitive, if so return false', () => {

    var input = "Password";
    
    expect(checkPasswordMatch(input)).toBe(false)
    
})