import React, {useEffect} from "react";
import {GLTFLoader} from "three/examples/jsm/loaders/GLTFLoader";
import {OrbitControls} from "three/examples/jsm/controls/OrbitControls";
import {AnimationMixer, Box3, Clock, Color, HemisphereLight, PerspectiveCamera, Scene, WebGLRenderer} from "three";
// import './ModelViewer.less'

const ModelViewer = ({src}) => {
	// if ( WEBGL.isWebGLAvailable() === false ) {
	// 	document.body.appendChild( WEBGL.getWebGLErrorMessage() );
	// }
	
	console.log(src)
	let container, controls;
	let camera, scene, renderer, light, bbox;
	let rotating = true;
	
	const clock = new Clock();
	let mixer = null;
	
	function init(qualifiedName, value) {
		if (!src) {
			return false;
		}
		container = document.getElementById(src);
		
		scene = new Scene();
		bbox = new Box3();
		// console.log(scene,bbox)
		
		scene.background = new Color(0xeeeeee);
		light = new HemisphereLight(0xbbbbff, 0x444422, 1.5);
		light.position.set(0, 1, 0);
		scene.add(light);
		
		
		const loader = new GLTFLoader();
		// console.log(src)
		loader.load(src, function (gltf) {
			// setContent(gltf.scene);
			// console.log(gltf.scene)
			URL.revokeObjectURL(src)
			// setContent(gltf.scene)
			scene.add(gltf.scene);
			mixer = new AnimationMixer(gltf.scene);
			console.log(gltf.animations.length);
			mixer.clipAction(gltf.animations[0]).play();
			console.dir(mixer.clipAction(gltf.animations[0]))
			render();
		}, undefined, function (e) {
			// console.error(e);
		});
		
		renderer = new WebGLRenderer({antialias: true});
		renderer.setPixelRatio(window.devicePixelRatio);
		// let model_container=document.getElementById(src)
		// renderer.setSize(model_container.offsetWidth , model_container.offsetHeight);
		renderer.gammaOutput = true;
		container.appendChild(renderer.domElement);
		// console.log(renderer.domElement)
		// window.addEventListener('resize', onWindowResize, false);
		camera = new PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.01, 1000);
		camera.position.set(0, 0, 400);
		
		controls = new OrbitControls(camera, renderer.domElement);
		controls.target.set(0, 0, 0);
		controls.update();
	}
	
	function render() {
		requestAnimationFrame(render);
		const delta = clock.getDelta();
		if (mixer != null) {
			mixer.update(delta);
		}
		renderer.render(scene, camera);
		mixer.update(clock.getDelta());
	}
	
	// function onWindowResize() {
	// 	camera.aspect = window.innerWidth / window.innerHeight;
	// 	camera.updateProjectionMatrix();
	// 	renderer.setSize(window.innerWidth, window.innerHeight);
	// }
	
	function animate() {
		requestAnimationFrame(animate);
		if (rotating) {
			scene.rotation.y += -0.005;
		}
		renderer.render(scene, camera);
	}
	
	function pauseRotation() {
		const modelBorder = document.getElementById(src);
		modelBorder.addEventListener("mouseenter", function (event) {
			rotating = false;
		});
		modelBorder.addEventListener("mouseleave", function (event) {
			rotating = true;
		});
		modelBorder.addEventListener('touchmove', function (e) {
			rotating = false;
		}, false);
		modelBorder.addEventListener('touchstart', function (e) {
			rotating = false;
		}, false);
		modelBorder.addEventListener('touchend', function (e) {
			rotating = true;
		}, false);
		
	}
	
	/**
	 * 开始Three
	 */
	useEffect(() => {
		init();
		animate();
		pauseRotation();
	}, [])
	
	return (
		<div id={src} style={{width: '100%', height: '100%'}} className='model-viewer'/>
	);
}

export default ModelViewer
