CSP adds some new functions for Python apps, and here is the full list of them with argument names and return types. Each time function requires a vector argument, such as vec2, vec3 or vec4, you can pass either a corresponding amount of numbers directly, or pass them packed in a tuple.

See also official and inofficial python docs: https://assettocorsamods.net/threads/doc-python-doc.59/
Shared memory reference: https://assettocorsamods.net/threads/doc-shared-memory-reference.58/
A getting started guide: https://assettocorsamods.net/threads/getting-started-with-ac-app-developing.716/#post-2892

```py
# Track controls:

def ac.ext_applyTrackConfig(config: str, flags: int):
  # flags: 1<<0 for restore conditions, 1<<1 for partial update
def ac.ext_setTrackConditionInput(conditionName: str, value: float):

# Mirrors (requires Real Mirror enabled):

def ac.ext_mirrorLeft():
def ac.ext_mirrorRight():
def ac.ext_mirrorUp():
def ac.ext_mirrorDown():
def ac.ext_mirrorFovUp():
def ac.ext_mirrorFovDown():
def ac.ext_mirrorAspectRatioUp():
def ac.ext_mirrorAspectRatioDown():
def ac.ext_mirrorToggleMon():
def ac.ext_mirrorPrev():
def ac.ext_mirrorNext():
def ac.ext_mirrorCurrent() -> int:
def ac.ext_mirrorParams() -> (isMonitor: bool, fov: float, aspectMult: float, role: int, index: int):

# Flipping mirrors (available since 0.1.76, 1 for horizontal flip, 2 for vertical, 3 for both):

def ac.ext_mirrorGetFlip() -> int:
def ac.ext_mirrorSetFlip(flip: int) -> int:

# G27 LEDs:

def ac.ext_isG27Available() -> bool:
def ac.ext_setG27Thresholds(minRpm: float, maxRpm: float):

# General functions:

def ac.ext_patchVersion() -> str:
def ac.ext_patchVersionCode() -> int:

def ac.ext_weatherDebugText() -> str:

def ac.ext_setStrictMode():    # activates strict mode with better error reporting, recommended
def ac.ext_pauseWhenHidden():  # allows app to pause when it’s not active
def ac.ext_isAnyAppVisible() -> bool:
def ac.ext_isAppVisible(appName: str) -> bool:

def ac.ext_perfBegin(key: str?):
  # starts measuring time
def ac.ext_perfEnd(key: str?) -> float:
  # stops measuring time, returns time in milliseconds, shows it in Python Debug app

def ac.ext_loadIniFileAsJson(filename: str, includeDir0: str?, includeDir1: str?, includeDir2: str?) -> str:
  # question mark means parameter is optional
def ac.ext_parseIniAsJson(iniData: str) -> str:

def ac.ext_getBaseAltitude() -> float:
def ac.ext_getAltitude(car: int) -> float:

def ac.ext_setDriverVisible(visible: bool, carIndex: int):
def ac.ext_setDoorsOpen(doorOpen: bool, carIndex: int):

def ac.ext_isExtendedPhysics(car: int) -> bool:
def ac.ext_getTyreGrain(car: int, tyre: int) -> float:
def ac.ext_getHeadlights(car: int) -> bool:
def ac.ext_getHandbrake(car: int) -> float:
def ac.ext_getTyreIsHot(car: int, tyre: int) -> bool:
def ac.ext_getTyreTempMult(car: int, tyre: int) -> float:
def ac.ext_getTyreBlister(car: int, tyre: int) -> float:
def ac.ext_getTyreFlatSpot(car: int, tyre: int) -> float:
def ac.ext_getTyreVirtualKM(car: int, tyre: int) -> float:
def ac.ext_getTyreCarcassTemp(car: int, tyre: int) -> float:

def ac.ext_getSuspensionTravel(corner: int) -> float:  # ! broken until and including csp 0.1.77-prev80
def ac.ext_getDamperTravel(corner: int) -> float:      # ! broken until and including csp 0.1.77-prev80

def ac.ext_getTcSetting1(car: int) -> int:
def ac.ext_getTcSetting2() -> int:
def ac.ext_getAeroSpeed() -> float:
def ac.ext_getDrag() -> float:
def ac.ext_getDownforce(selection: int) -> float:
def ac.ext_getStaticDeflection() -> float:
def ac.ext_getCurrentTorque() -> float:
def ac.ext_getBrakeCoreTemp(corner: int) -> float:
def ac.ext_getSteerTorque() -> float:
def ac.ext_getBrakeTorque(corner: int) -> float:
def ac.ext_getTireLoadedRadius(corner: int) -> float:

def ac.ext_isTripleScreenCamera() -> bool:
def ac.ext_isInVR() -> bool:
def ac.ext_getCameraDirection() -> vec3:  # vec3 is a tuple with 3 elements
def ac.ext_getCameraPosition() -> vec3:
def ac.ext_setCameraPosition(pos: vec3):
def ac.ext_getCameraPositionAxis(axis: int) -> float:
def ac.ext_setCameraPositionAxis(axis: int, value: float):
def ac.ext_setCameraDirection(forward: vec3, up: vec3?):
def ac.ext_getCameraMatrix() -> mat4x4:  # mat4x4 is a tuple with 16 elements
def ac.ext_getCameraRollRad() -> float:  # rad means result is in radians
def ac.ext_getCameraPitchRad() -> float:
def ac.ext_getCameraYawRad() -> float:
def ac.ext_getCameraFov() -> float:
def ac.ext_setCameraFov(value: float):
def ac.ext_getCameraDofFactor() -> float:
def ac.ext_setCameraDofFactor(value: float):
def ac.ext_getCameraDofFocus() -> float:
def ac.ext_setCameraDofFocus(value: float):
def ac.ext_getCameraClipNear() -> float:
def ac.ext_setCameraClipNear(value: float):
def ac.ext_getCameraClipFar() -> float:
def ac.ext_setCameraClipFar(value: float):
def ac.ext_currentPpFilter() -> str:

def ac.ext_getReplayFrameMS() -> float:  # frame time in ms
def ac.ext_getReplayFrames() -> int:     # number of recorded frames
def ac.ext_getReplayPosition() -> int:   # frame index
def ac.ext_setReplayPosition(frameIndex: int):

def ac.ext_getCurrentCamera() -> int:
def ac.ext_setCurrentCamera(mode: int):
def ac.ext_getCurrentDrivableCamera() -> int:
def ac.ext_setCurrentDrivableCamera(mode: int):
def ac.ext_getTrackCamerasNumber() -> int:
def ac.ext_getCurrentTrackCamera() -> int:
def ac.ext_setCurrentTrackCamera(setIndex: int):
def ac.ext_getAudioVolume() -> float:
def ac.ext_setAudioVolume(volume: float):

def ac.ext_getPreviousSectorTime() -> str:
def ac.ext_getCurrentSector() -> int:

def ac.ext_isButtonPressed(keyIndex: int) -> bool:
def ac.ext_isCtrlPressed() -> bool:
def ac.ext_isAltPressed() -> bool:
def ac.ext_isShiftPressed() -> bool:
def ac.ext_isJoystickButtonPressed(controllerIndex: int, buttonIndex: int) -> bool:
def ac.ext_getJoystickAxisValue(controllerIndex: int, axisIndex: int) -> float:
def ac.ext_getJoystickDpadValue(controllerIndex: int, dpadIndex: int) -> int:

def ac.ext_setClipboardData(text: str):
def ac.ext_isVirtualMirrorForced() -> bool:
def ac.ext_markLapAsSpoiled():
def ac.ext_getCameraPositionRelativeToCar() -> vec3:
def ac.ext_getCompassAngle(direction: vec3) -> float:
  # turns direction into heading angle in degrees
def ac.ext_dirname() -> str:
  # path to python app folder
def ac.ext_getSplineLength(splineIndex: int) -> float:
  # 0 for main spline (so, length of the whole track), 1 for pits spline
def ac.ext_worldToSpline(splineIndex: int, worldPos: vec3) -> float:
def ac.ext_splineToWorld(splineIndex: int, splinePos: float) -> vec3:

def ac.ext_storeLua(key: str, value: float or string):
def ac.ext_loadLua(key: str) -> float or string:

def ac.ext_getStateAbs(carIndex: int) -> int:
def ac.ext_getStateAbsActive(carIndex: int) -> bool:
def ac.ext_getStateTc(carIndex: int) -> int:
def ac.ext_getStateTcActive(carIndex: int) -> bool:

def ac.ext_pauseFsWatching():
def ac.ext_resumeFsWatching():

def ac.ext_resetCar():       # resets car to the road invalidating lap
def ac.ext_takeAStepBack():  # moves car back invalidating lap
def ac.ext_weatherFxActive() -> bool:
def ac.ext_weatherTimeOffset(offset: float) -> bool:
def ac.ext_getWeatherTimeMult() -> float:
def ac.ext_setWeatherTimeMult(value: float):
def ac.ext_isVaoPatchLoaded() -> bool:
def ac.ext_vaoOnly():
def ac.ext_vaoNormalDebug():
def ac.ext_vaoDisable():
def ac.ext_vaoNormal():
def ac.ext_setVaoActive(active: bool):

def ac.ext_getWiperSpeedsNumber() -> int:
def ac.ext_getWiperSpeed() -> int:
def ac.ext_setWiperSpeed(wiperSpeed: int):

def ac.ext_getCameraProj() -> mat4x4:
def ac.ext_getCameraView() -> mat4x4:
def ac.ext_getLightsNum() -> int:
def ac.ext_getCarLightsNum() -> int:
def ac.ext_getTrackLightsNum() -> int:
def ac.ext_getLightsVisible() -> int:
def ac.ext_getCarLightsVisible() -> int:
def ac.ext_getTrackLightsVisible() -> int:
def ac.ext_getLightsMirrorVisible() -> int:
def ac.ext_getCarLightsMirrorVisible() -> int:
def ac.ext_getTrackLightsMirrorVisible() -> int:
def ac.ext_getAmbientMult() -> float:
def ac.ext_getAngleSpeed() -> float:
def ac.ext_debugLights(nameFilter: str, count: int, distance: float, mode: int):

# Extended render functions:

def ac.ext_glSetCullMode(mode: int):
  # mode: 0 for front, 1 for back, 2 for no culling, 4 for wireframe, 7 for antialiased wireframe
def ac.ext_glSetBlendMode(mode: int):
  # mode: 0 for opaque, 1 for alpha blend, 2 for alpha test, 4 for additive, 5 for multiplicative
def ac.ext_mirrorTexture() -> int:
  # returns texture index which can be used the same as ac.createTexture()
def ac.ext_releaseMirrorTexture():
  # call it for each call of ac.ext_mirrorTexture() when texture is no longer needed to re-activate
  # real mirrors
def ac.ext_createRenderTarget(width: int, height: int, mips: bool) -> int:
  # returns texture index, but also this number can be used to draw things to
def ac.ext_clearRenderTarget(rtIndex: int):
def ac.ext_generateMips(rtIndex: int):
def ac.ext_disposeRenderTarget(rtIndex: int):
def ac.ext_bindRenderTarget(rtIndex: int):
  # starts drawing into render target
def ac.ext_restoreRenderTarget():
  # restores original render target to continue drawing app to
def ac.ext_glSetTexture(textureIndex: int, slotIndex: int):
  # binds texture
def ac.ext_glLoadPixelShader(filename: str) -> int:
  # loads pixel shader (there is an example at the bottom of this post)
def ac.ext_glSetPixelShader(shaderIndex: int):
  # custom shader will be used for further draw calls
def ac.ext_glResetPixelShader():
  # reverts to original pixel shader
def ac.ext_glVertexTex(posUV: vec4):
  # adds a new vertex with texture coordinates, use with ac.glBegin() and ac.glEnd()
  # vec4 is a tuple with four values
def ac.ext_glTexCoord2f(uv: vec2):
  # adds texture coordinates to previously added vertex
  # vec2 is a tuple with two values
def ac.ext_glFontCreate(font: str, size: float, italic: int, weight: int) -> int:
def ac.ext_glFontColor(fontIndex: int, color: vec4):
def ac.ext_glFontUse(fontIndex: int, text: str, pos: vec2, scale: float, alignment: int):
  # uses created font to draw some text
  # alignment: 0 for left, 1 for right, 2 for center

```

# Example shader for custom drawing

```c
// Default AC texture samplers bound by default:

SamplerState samPoint : register(s2) {
  Filter = POINT;
  AddressU = WRAP;
  AddressV = WRAP;
};

SamplerState samLinear : register(s5) {
  Filter = LINEAR;
  AddressU = WRAP;
  AddressV = WRAP;
};

struct VS_IN {
  float4 PosH : SV_POSITION;
  float4 Color : COLOR;
  float2 Tex : TEXCOORD;
  float3 Tangent : TANGENT;
};

// Regular texture to draw:

Texture2D txDiffuse : register(t0);

// Actual code:

float4 main(VS_IN pin) : SV_TARGET {
  return 1 - txDiffuse.Sample(samLinear, pin.Tex); // simple inversion for an example
}
```
