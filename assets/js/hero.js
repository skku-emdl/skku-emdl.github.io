/* EMDL hero: corner-sharing BX6 octahedra of a cubic ABX3 perovskite, lit by warm "sunlight". */
(function () {
  var host = document.getElementById('lattice');
  if (!host || !window.THREE) return;
  var T = window.THREE;
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  var renderer;
  try {
    renderer = new T.WebGLRenderer({ antialias: true, alpha: true });
  } catch (e) { host.classList.add('no-gl'); return; }
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
  renderer.outputColorSpace = T.SRGBColorSpace;
  renderer.toneMapping = T.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.05;
  host.appendChild(renderer.domElement);

  var scene = new T.Scene();
  var camera = new T.PerspectiveCamera(32, 1, 0.1, 100);
  camera.position.set(10.5, 7.0, 12.8);
  camera.lookAt(0, 0, 0);

  // light: warm sun from upper left, cool sky fill, faint rim
  scene.add(new T.HemisphereLight(0x9fb7ff, 0x1a1408, 0.55));
  var sun = new T.DirectionalLight(0xffd59a, 2.4);
  sun.position.set(-6, 10, 6);
  scene.add(sun);
  var rim = new T.DirectionalLight(0x5f86ff, 1.2);
  rim.position.set(8, -2, -8);
  scene.add(rim);
  var glint = new T.PointLight(0xffe2b0, 18, 14, 2);
  scene.add(glint);

  var lattice = new T.Group();
  scene.add(lattice);

  var N = 3, a = 2.0, off = (N - 1) * a / 2;
  var octGeo = new T.OctahedronGeometry(a / 2 * 0.98, 0);
  var octMat = new T.MeshPhysicalMaterial({
    color: 0xd9892b, roughness: 0.28, metalness: 0.05, transmission: 0.35, thickness: 0.6,
    transparent: true, opacity: 0.88, clearcoat: 0.6, clearcoatRoughness: 0.25, flatShading: true
  });
  var edgeGeo = new T.EdgesGeometry(octGeo);
  var edgeMat = new T.LineBasicMaterial({ color: 0xffe3b5, transparent: true, opacity: 0.55 });
  var bGeo = new T.SphereGeometry(0.16, 20, 16);
  var bMat = new T.MeshStandardMaterial({ color: 0x3b2a1a, roughness: 0.4 });
  var xGeo = new T.SphereGeometry(0.12, 16, 12);
  var xMat = new T.MeshStandardMaterial({ color: 0xf3efe6, roughness: 0.35 });
  var aGeo = new T.SphereGeometry(0.42, 32, 24);
  var aMat = new T.MeshPhysicalMaterial({ color: 0x4f7dff, roughness: 0.15, clearcoat: 1, emissive: 0x1a3cb0, emissiveIntensity: 0.35 });

  var xSeen = {};
  function key(v) { return [v.x, v.y, v.z].map(function (n) { return Math.round(n * 100); }).join(','); }
  var dirs = [[1,0,0],[-1,0,0],[0,1,0],[0,-1,0],[0,0,1],[0,0,-1]];
  for (var i = 0; i < N; i++) for (var j = 0; j < N; j++) for (var k = 0; k < N; k++) {
    var p = new T.Vector3(i * a - off, j * a - off, k * a - off);
    var o = new T.Mesh(octGeo, octMat); o.position.copy(p); lattice.add(o);
    var ed = new T.LineSegments(edgeGeo, edgeMat); ed.position.copy(p); lattice.add(ed);
    var b = new T.Mesh(bGeo, bMat); b.position.copy(p); lattice.add(b);
    dirs.forEach(function (d) {
      var q = p.clone().add(new T.Vector3(d[0], d[1], d[2]).multiplyScalar(a / 2));
      var kq = key(q);
      if (!xSeen[kq]) { xSeen[kq] = 1; var x = new T.Mesh(xGeo, xMat); x.position.copy(q); lattice.add(x); }
    });
  }
  for (i = 0; i < N - 1; i++) for (j = 0; j < N - 1; j++) for (k = 0; k < N - 1; k++) {
    var c = new T.Mesh(aGeo, aMat);
    c.position.set((i + 0.5) * a - off, (j + 0.5) * a - off, (k + 0.5) * a - off);
    lattice.add(c);
  }
  lattice.rotation.set(0.12, 0.6, 0);

  function resize() {
    var w = host.clientWidth, h = host.clientHeight;
    if (!w || !h) return;
    renderer.setSize(w, h, false);
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
  }
  resize();
  window.addEventListener('resize', resize);
  if ('ResizeObserver' in window) new ResizeObserver(resize).observe(host);

  var mx = 0, my = 0;
  host.addEventListener('pointermove', function (ev) {
    var r = host.getBoundingClientRect();
    mx = (ev.clientX - r.left) / r.width - 0.5;
    my = (ev.clientY - r.top) / r.height - 0.5;
  });
  host.addEventListener('pointerleave', function () { mx = 0; my = 0; });

  var visible = true;
  if ('IntersectionObserver' in window) {
    new IntersectionObserver(function (es) { visible = es[0].isIntersecting; }).observe(host);
  }

  var t0 = performance.now();
  function frame(now) {
    var t = (now - t0) / 1000;
    if (visible) {
      lattice.rotation.y = 0.6 + t * 0.12 + mx * 0.5;
      lattice.rotation.x = 0.12 + Math.sin(t * 0.3) * 0.05 + my * 0.3;
      glint.position.set(Math.cos(t * 0.6) * 6, 4 + Math.sin(t * 0.9) * 1.5, Math.sin(t * 0.6) * 6);
      renderer.render(scene, camera);
    }
    if (!reduce) requestAnimationFrame(frame);
  }
  if (reduce) { glint.position.set(-3, 5, 5); renderer.render(scene, camera); }
  else requestAnimationFrame(frame);
})();
