package com.atra.bahar.bugsdetector.Model

data class BugsDetectorDTO (
    // Class that provides the same data that the BugsDetector api uses
    var fly : String? = null,
    var bigMosquito : String? = null,
    var normalMosquito : String? = null,
    var tinyMosquito : String? = null) {

}