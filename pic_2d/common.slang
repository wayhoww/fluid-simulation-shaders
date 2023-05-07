static constexpr uint PARTICLES_PER_GRID_CELL = 9;
static constexpr float GRID_CELL_SIZE = 0.1f;
static constexpr float DELTA_TIME = 1 / 60.0f;

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

struct StaticVariables {
    int frame_count;
    uint2 grid_size;

    uint get_particle_count() {
        return (this.grid_size.x - 1) * (this.grid_size.y - 1) * PARTICLES_PER_GRID_CELL;
    }

    bool is_the_first_frame() {
        return this.frame_count == 1;
    }
};

RWStructuredBuffer<StaticVariables> Static;

StaticVariables get_static_variables() {
    return Static[0];
}

void set_static_variables(StaticVariables v) {
    Static[0] = v;
}

struct ParticleData {
    float2 velocity;
    float2 location;

    [mutating]
    void set_location_from_grid(float2 grid_loc) {
        this.location = grid_loc * GRID_CELL_SIZE;
    }

    float2 get_grid_location() {
        return this.location / GRID_CELL_SIZE;
    }

    bool inside_boundary() {
        let grid_location = get_grid_location();
        let grid_size = get_static_variables().grid_size;
        return grid_location.x >= 0 && grid_location.x < grid_size.x - 1 && grid_location.y >= 0 && grid_location.y < grid_size.y - 1;
    }
};

vector<int, N> encode_fixed_point<let N : int>(vector<float, N> x) {
    return vector<int, N>(round(x * 10000));
}

vector<float, N> decode_fixed_point<let N : int>(vector<int, N> x) {
    return vector<float, N>(x) / 10000;
}

int encode_fixed_point(float x) {
    return int(round(x * 10000));
}

float decode_fixed_point(int x) {
    return float(x) / 10000;
}

float linear_bspine(float x) {
    return abs(x) < 1 ? 1 - abs(x) : 0;
}

extension Texture2D<float4> {
    float4 Load(float2 pos) {
        int2 pos00 = int2(pos);
        int2 pos01 = pos00 + int2(0, 1);
        int2 pos10 = pos00 + int2(1, 0);
        int2 pos11 = pos00 + int2(1, 1);

        float4 data00 = this.Load(int3(pos00, 0));
        float4 data01 = this.Load(int3(pos01, 0));
        float4 data10 = this.Load(int3(pos10, 0));
        float4 data11 = this.Load(int3(pos11, 0));

        float4 data0 = lerp(data01, data00, pos11.y - pos.y);
        float4 data1 = lerp(data11, data10, pos11.y - pos.y);

        float4 data = lerp(data1, data0, pos11.x - pos.x);

        return data;
    }
}
