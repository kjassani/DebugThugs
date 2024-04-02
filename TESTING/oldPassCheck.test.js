const oldPassCheck = require('./oldPassCheck')

test('Tests if password matches previous password, if so return true', () => {

    var input = "password";
    
    expect(oldPassCheck(input)).toBe(true)
    
})

test('Tests if password does not match previous password, if so return false', () => {

    var input = "123";
    
    expect(oldPassCheck(input)).toBe(false)
    
})

test('Tests if password does not match previous password, case-sensitive,if so return false', () => {

    var input = "Password";
    
    expect(oldPassCheck(input)).toBe(false)
    
})