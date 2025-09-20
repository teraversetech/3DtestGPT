"use client";

import { useEffect, useRef } from "react";
import * as THREE from "three";
import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader";

interface ThreeViewerProps {
  src: string;
  poster: string;
}

export function ThreeViewer({ src, poster }: ThreeViewerProps) {
  const containerRef = useRef<HTMLDivElement | null>(null);
  const mounted = useRef(false);

  useEffect(() => {
    if (!containerRef.current || mounted.current) return;
    mounted.current = true;

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(45, 1, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(360, 360);
    containerRef.current.appendChild(renderer.domElement);

    const light = new THREE.HemisphereLight(0xffffff, 0x444444, 1);
    scene.add(light);
    const directional = new THREE.DirectionalLight(0xffffff, 0.8);
    directional.position.set(1, 1, 1);
    scene.add(directional);

    const loader = new GLTFLoader();
    loader.load(
      src,
      (gltf) => {
        scene.add(gltf.scene);
        const box = new THREE.Box3().setFromObject(gltf.scene);
        const size = box.getSize(new THREE.Vector3()).length();
        const center = box.getCenter(new THREE.Vector3());
        camera.position.set(center.x + size, center.y + size, center.z + size);
        camera.lookAt(center);
        const animate = () => {
          requestAnimationFrame(animate);
          gltf.scene.rotation.y += 0.005;
          renderer.render(scene, camera);
        };
        animate();
      },
      undefined,
      () => {
        const textureLoader = new THREE.TextureLoader();
        const plane = new THREE.Mesh(
          new THREE.PlaneGeometry(2, 2),
          new THREE.MeshBasicMaterial({ map: textureLoader.load(poster) })
        );
        scene.add(plane);
        camera.position.set(0, 0, 2);
        renderer.render(scene, camera);
      }
    );

    return () => {
      renderer.dispose();
      containerRef.current?.removeChild(renderer.domElement);
    };
  }, [src, poster]);

  return <div ref={containerRef} className="h-[360px] w-full" aria-label="3D preview" />;
}
