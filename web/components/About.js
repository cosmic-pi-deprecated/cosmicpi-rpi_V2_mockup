window.About = Vue.component('about', {
  template: `
    <div style="max-width: 600px; margin: auto; padding: 8px; text-align: center;">
		<p><img src="images/device.jpg" style="width: 100%" /></p>
		
		<p>{{ $t("description") }}</p>
    </div>
  `
});
