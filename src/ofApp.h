#pragma once

#include "ofMain.h"
#include "ofxOsc.h"

#define PORT 9000
#define FFT_BINS 64

class ofApp : public ofBaseApp {
public:
    void setup();
    void update();
    void draw();

    ofShader shader;
    ofImage yantra;
    ofFbo fbo;

    ofxOscReceiver receiver;
    std::vector<float> fftData;
};
