using System;
using System.Collections.Generic;
using System.Linq;

namespace RealEstateVR
{
    public class RoomNode
    {
        public string RoomName { get; set; }
        public float Length { get; set; }
        public float Width { get; set; }
        public float Height { get; set; }
        public List<string> Features { get; set; }

        public RoomNode(string roomName, float length, float width, float height)
        {
            RoomName = roomName;
            Length = length;
            Width = width;
            Height = height;
            Features = new List<string>();
        }

        public float CalculateFloorArea() => Length * Width;
        public float CalculateCubicVolume() => Length * Width * Height;
    }

    public class CameraHotspot
    {
        public string HotspotId { get; set; }
        public string TargetRoomName { get; set; }
        public float PositionX { get; set; }
        public float PositionY { get; set; }
        public float PositionZ { get; set; }

        public CameraHotspot(string id, string roomName, float x, float y, float z)
        {
            HotspotId = id;
            TargetRoomName = roomName;
            PositionX = x;
            PositionY = y;
            PositionZ = z;
        }
    }

    public class VirtualPropertyTourEngine
    {
        public string PropertyId { get; private set; }
        public string PropertyTitle { get; private set; }
        private readonly List<RoomNode> _rooms;
        private readonly List<CameraHotspot> _hotspots;
        public bool IsRenderingVR { get; private set; }

        public VirtualPropertyTourEngine(string propertyId, string propertyTitle)
        {
            PropertyId = propertyId;
            PropertyTitle = propertyTitle;
            _rooms = new List<RoomNode>();
            _hotspots = new List<CameraHotspot>();
            IsRenderingVR = false;
        }

        public void AddRoom(RoomNode room)
        {
            _rooms.Add(room);
            Console.WriteLine($"[Engine] Added room '{room.RoomName}' ({room.CalculateFloorArea()} sq meters)");
        }

        public void AddHotspot(CameraHotspot hotspot)
        {
            _hotspots.Add(hotspot);
        }

        public void StartVirtualRealitySession()
        {
            if (!_rooms.Any())
            {
                throw new InvalidOperationException("Cannot start VR session without room data.");
            }
            IsRenderingVR = true;
            Console.WriteLine($"\n=== VR Session Activated for: {PropertyTitle} ===");
            Console.WriteLine($"Total Rendered Floor Area: {CalculateTotalArea()} sq meters");
            Console.WriteLine($"Total Interactive Hotspots: {_hotspots.Count}");
        }

        public void TeleportToHotspot(string hotspotId)
        {
            var target = _hotspots.FirstOrDefault(h => h.HotspotId == hotspotId);
            if (target == null)
            {
                Console.WriteLine($"[Error] Hotspot '{hotspotId}' not found.");
                return;
            }
            Console.WriteLine($"[Camera Teleport] Camera moved to {target.TargetRoomName} at Coordinates ({target.PositionX}, {target.PositionY}, {target.PositionZ})");
        }

        public float CalculateTotalArea() => _rooms.Sum(r => r.CalculateFloorArea());

        public void RenderCreatorWalkthroughScript()
        {
            Console.WriteLine("\n--- Creator Video Walkthrough Sequence ---");
            int step = 1;
            foreach (var room in _rooms)
            {
                Console.WriteLine($"Step {step++}: Camera pans around {room.RoomName}. Area: {room.CalculateFloorArea()} sqm. Features: {string.Join(", ", room.Features)}");
            }
        }
    }

    public class Program
    {
        public static void Main()
        {
            var tourEngine = new VirtualPropertyTourEngine("PROP-9901", "Penthouse Suite A");

            var livingRoom = new RoomNode("Living Room", 8.5f, 6.0f, 3.2f);
            livingRoom.Features.AddRange(new[] { "Floor-to-ceiling windows", "Hardwood flooring", "Smart lighting" });

            var masterBedroom = new RoomNode("Master Bedroom", 5.5f, 4.5f, 3.0f);
            masterBedroom.Features.AddRange(new[] { "Walk-in closet", "En-suite bathroom access" });

            tourEngine.AddRoom(livingRoom);
            tourEngine.AddRoom(masterBedroom);

            tourEngine.AddHotspot(new CameraHotspot("HS-01", "Living Room", 0.0f, 1.6f, 2.0f));
            tourEngine.AddHotspot(new CameraHotspot("HS-02", "Master Bedroom", 10.5f, 1.6f, 8.2f));

            tourEngine.StartVirtualRealitySession();
            tourEngine.TeleportToHotspot("HS-01");
            tourEngine.RenderCreatorWalkthroughScript();
        }
    }
}