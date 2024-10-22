document.addEventListener("DOMContentLoaded", function () {
    setTimeout(function () {
        // Find all <script type="math/tex"> tags
        var mathScripts = document.querySelectorAll('script[type="math/tex"], script[type="math/tex; mode=display"]');

        mathScripts.forEach(function (script) {
            // Extract the LaTeX content
            var texContent = script.textContent || script.innerText;

            // Create a span to insert the rendered KaTeX
            var span = document.createElement('span');

            try {
                // Render the LaTeX using KaTeX
                katex.render(texContent, span, {
                    throwOnError: false
                });
            } catch (err) {
                span.innerHTML = 'Error rendering LaTeX';
            }

            // Replace the <script> tag with the rendered span
            script.parentNode.replaceChild(span, script);
    }, 1000);
    });
});
