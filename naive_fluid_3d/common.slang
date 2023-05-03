cbuffer PerFrameCB
{
    uint3 iThreads;
    uint2 iResolution; // graphics pass only

    float iTime;
    float iDeltaTime;
    
    float2 iMousePosition;
    int2 iMouseCoordinate;
    int2 iMouseLastCoordinate;
    bool iMouseLeftButtonDown;

    float3 iCameraPosition;
    float3 iCameraU;
    float3 iCameraV;
    float3 iCameraW;

    uint2 iFrameDim;
};

struct Ray {
    float3 origin;
    float3 direction;
};

Ray get_camera_ray(float2 uv) {

    // Compute sample position in screen space in [0,1] with origin at the top-left corner.
    // The camera jitter offsets the sample by +-0.5 pixels from the pixel center.
    // float2 p = (pixel + float2(0.5f, 0.5f)) / frameDim;
    // if (applyJitter) p += float2(-data.jitterX, data.jitterY);
    // float2 ndc = float2(2, -2) * p + float2(-1, 1);

    // Compute the non-normalized ray direction assuming a pinhole camera.
    // return ndc.x * data.cameraU + ndc.y * data.cameraV + data.cameraW;

    float2 ndc = float2(2, -2) * uv + float2(-1, 1);

    Ray ray;
    ray.origin = iCameraPosition;
    ray.direction = normalize(ndc.x * iCameraU + ndc.y * iCameraV + iCameraW);
    return ray;
}

extension Texture3D<float4> {
    float4 Load(float3 pos) {
        int3 pos000 = int3(pos);
        int3 pos001 = pos000 + int3(0, 0, 1);
        int3 pos010 = pos000 + int3(0, 1, 0);
        int3 pos011 = pos000 + int3(0, 1, 1);
        int3 pos100 = pos000 + int3(1, 0, 0);
        int3 pos101 = pos000 + int3(1, 0, 1);
        int3 pos110 = pos000 + int3(1, 1, 0);
        int3 pos111 = pos000 + int3(1, 1, 1);

        float4 data000 = this.Load(int4(pos000, 0));
        float4 data001 = this.Load(int4(pos001, 0));
        float4 data010 = this.Load(int4(pos010, 0));
        float4 data011 = this.Load(int4(pos011, 0));
        float4 data100 = this.Load(int4(pos100, 0));
        float4 data101 = this.Load(int4(pos101, 0));
        float4 data110 = this.Load(int4(pos110, 0));
        float4 data111 = this.Load(int4(pos111, 0));

        float4 data00 = lerp(data000, data001, pos.z - pos000.z);
        float4 data01 = lerp(data010, data011, pos.z - pos000.z);
        float4 data10 = lerp(data100, data101, pos.z - pos000.z);
        float4 data11 = lerp(data110, data111, pos.z - pos000.z);
        
        float4 data0 = lerp(data00, data01, pos.y - pos000.y);
        float4 data1 = lerp(data10, data11, pos.y - pos000.y);

        float4 data = lerp(data0, data1, pos.x - pos000.x);

        return data;
    }

    uint3 GetDimensions() {
        uint x, y, z;
        this.GetDimensions(x, y, z);
        return uint3(x, y, z);
    }

    float4 SampleLevel0(float3 pos) {
        return this.Load(pos * this.GetDimensions());
    }
}

constexpr static float CELL_SIZE = 0.1f;
constexpr static float DELTA_TIME = 0.0166666f;