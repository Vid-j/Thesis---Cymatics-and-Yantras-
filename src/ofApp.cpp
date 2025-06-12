#include "ofApp.h"

void ofApp::setup(){
    ofSetWindowTitle("Cymatic Yantra Overlay");
    ofSetFrameRate(60);
    ofBackground(0);

    receiver.setup(PORT);

    yantra.load("yantra.png");
    fbo.allocate(ofGetWidth(), ofGetHeight());

    shader.load("shaders/cymatic.vert", "shaders/cymatic.frag");

    fftData.resize(FFT_BINS, 0.0f);
}

void ofApp::update(){
    while (receiver.hasWaitingMessages()) {
        ofxOscMessage m;
        receiver.getNextMessage(m);
        if (m.getAddress() == "/fft") {
            for (int i = 0; i < std::min(m.getNumArgs(), FFT_BINS); ++i) {
                fftData[i] = m.getArgAsFloat(i);
            }
        }
    }
}

void ofApp::draw(){
    fbo.begin();
    shader.begin();
    shader.setUniformTexture("u_yantra", yantra.getTexture(), 1);
    shader.setUniform1fv("u_fft", fftData.data(), FFT_BINS);
    shader.setUniform2f("u_resolution", ofGetWidth(), ofGetHeight());
    shader.setUniform1f("u_time", ofGetElapsedTimef());
    ofDrawRectangle(0, 0, ofGetWidth(), ofGetHeight());
    shader.end();
    fbo.end();

    fbo.draw(0, 0);
}
