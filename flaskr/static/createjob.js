$(document).ready(function() {
    var stage_counter = 1;
    var counter2 = 1;
    $('#add-stage').click(function(e) {
        $('#stages-fb').append(`<div class="field" id="st` + stage_counter + `">
          <div class="control">
              <div class="select is-fullwidth">
                  <select name="Stage_Description">
                      {%for key, value in stages.items()%}
                      <option value={{key}}>{{value}}</option>
                      {%endfor%}
                  </select>
              </div>
          </div>`
        );
        stage_counter++;

    });

    $('body').on('click', '#delete-stage', function(e) {
        e.preventDefault();
        $('#st' + (stage_counter - 1)).remove();
        stage_counter--;

    });


    $('body').on('click', '#add-skill', function(e) {
        $('#row').append(`		<div class="columns" id="col` + counter2 + `">
      <div class="column">
      <label class="label">Skill</label>
        <div class="control">
          <div class="select is-fullwidth">
            <select name="skill">
              <option>Python</option>
              <option>Java</option>
              <option>Haskell</option>
              <option>C</option>
              <option>HTML</option>
              <option>CSS</option>
              <option>javascript</option>
              <option>PHP</option>
              <option>C++</option>
            </select>
          </div>
        </div>
      </div>
      <div class="column">
      <label class="label">Proficiency</label>
        <div class="control">
                          <input name="skillVal" class="slider has-output is-fullwidth is-circle" min="1" max="10" value="1" step="1" type="range">
                        <output for="sliderWithValue">1</output>
        </div>
      </div>
  </div>
    `);
        counter2++;

    });

    $('body').on('click', '#delete-skill', function(e) {
        e.preventDefault();
        $('#col' + (counter2 - 1)).remove();
        counter2--;

    });


      $(document).on('change', 'input.slider',function () {
          $(this).next().html($(this).val());
      });


});

  $('body').on('click', '#add-skill', function(e) {
    function findOutputForSlider(element) {
        var idVal = element.id;
        outputs = document.getElementsByTagName('output');
        for (var i = 0; i < outputs.length; i++) {
            if (outputs[i].htmlFor == idVal)
                return outputs[i];
        }
    }

    function getSliderOutputPosition(slider) {
        // Update output position
        var newPlace,
            minValue;

        var style = window.getComputedStyle(slider, null);
        // Measure width of range input
        sliderWidth = parseInt(style.getPropertyValue('width'), 10);

        // Figure out placement percentage between left and right of input
        if (!slider.getAttribute('min')) {
            minValue = 0;
        } else {
            minValue = slider.getAttribute('min');
        }
        var newPoint = (slider.value - minValue) / (slider.getAttribute('max') - minValue);

        // Prevent bubble from going beyond left or right (unsupported browsers)
        if (newPoint < 0) {
            newPlace = 0;
        } else if (newPoint > 1) {
            newPlace = sliderWidth;
        } else {
            newPlace = sliderWidth * newPoint;
        }

        return {
            'position': newPlace + 'px'
        }
    }

    document.addEventListener('DOMContentLoaded', function() {
        // Get all document sliders
        var sliders = document.querySelectorAll('input[type="range"].slider');
        [].forEach.call(sliders, function(slider) {
            var output = findOutputForSlider(slider);
            if (output) {
                if (slider.classList.contains('has-output-tooltip')) {
                    // Get new output position
                    var newPosition = getSliderOutputPosition(slider);

                    // Set output position
                    output.style['left'] = newPosition.position;
                }

                // Add event listener to update output when slider value change
                slider.addEventListener('input', function(event) {
                    if (event.target.classList.contains('has-output-tooltip')) {
                        // Get new output position
                        var newPosition = getSliderOutputPosition(event.target);

                        // Set output position
                        output.style['left'] = newPosition.position;
                    }

                    // Update output with slider value
                    output.value = event.target.value;
                });
            }
        });
    });
    });
