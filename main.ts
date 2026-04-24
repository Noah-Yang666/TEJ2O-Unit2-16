/* Copyright (c) 2020 MTHS All rights reserved
 *
 * Created by: Noah Yang
 * Created on: April 2026
 * This program uses bluetooth to transmit messages
*/

// variables needed
let numberDistance: number = 0

// setting up
basic.showIcon(IconNames.Happy)
radio.setGroup(67)

// start tracking distance with button A
input.onButtonPressed(Button.A, function () {
    while (true) {

        // finding the distance with sonar
        basic.clearScreen()
        numberDistance = sonar.ping(
            DigitalPin.P1, // trigger pin
            DigitalPin.P2, // echo pin
            PingUnit.Centimeters
        )
        basic.showString((numberDistance) + " cm")
        basic.showIcon(IconNames.Square)

        if (numberDistance <= 5) {
            basic.showIcon(IconNames.Triangle)
            radio.sendString("Too Close")
        } else {
            basic.showIcon(IconNames.Triangle)
            radio.sendString("It's good")
        }
        pause(5000)
    }
})

radio.onReceivedString(function (receivedString) {
    basic.clearScreen()
    basic.showString(receivedString)
    basic.showIcon(IconNames.Happy)
})
