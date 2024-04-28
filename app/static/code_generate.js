document.addEventListener('DOMContentLoaded', function () {
    var propertySelect = document.getElementById('property_select');
    var codeTypeSelect = document.getElementById('code_type');
    var expirationDateResult = document.getElementById('expiration_date_result');
    var responseDataDiv = document.getElementById('response-data');
    // var properties = JSON.parse('{{ properties | tojson | safe }}');

    // 初始化页面时获取注册码属性并填充到下拉列表中
    populatePropertySelect(properties);

    // code类型选择的事件监听器
    codeTypeSelect.addEventListener('change', function () {
        expirationDateResult.innerText = '';
        responseDataDiv.innerText = '';
        updatePropertyOptions(); // 根据注册码类型更新属性选项
        // 更新属性选项时设置属性选择框为默认值
        setDefaultProperty();
    });

    // 触发一次change事件，以确保在页面加载时更新属性选项
    codeTypeSelect.dispatchEvent(new Event('change'));

    // 根据注册码类型更新属性选项
    function updatePropertyOptions() {
        var selectedType = codeTypeSelect.value;
        var options = propertySelect.options;

        // 遍历下拉列表中的选项，根据注册码类型隐藏或显示相应类型的属性
        for (var i = 0; i < options.length; i++) {
            var option = options[i];
            if (option.dataset.type === selectedType || option.dataset.type === '') {
                option.style.display = 'block'; // 显示与注册码类型匹配的属性选项
            } else {
                option.style.display = 'none'; // 隐藏不匹配的属性选项
            }
        }
    }

    function populatePropertySelect(properties) {
        // 清空下拉列表
        propertySelect.innerHTML = '';

        // 如果属性列表为空，添加一个空的选项
        if (properties.length === 0) {
            var emptyOption = document.createElement('option');
            emptyOption.value = '';
            emptyOption.textContent = 'No properties available';
            propertySelect.appendChild(emptyOption);
        } else {
            // 遍历属性数据并添加到下拉列表中
            properties.forEach(property => {
                var option = document.createElement('option');
                option.value = property[0];
                option.textContent = property[1] + ' (' + property[4] + ')';
                option.dataset.type = property[4]; // 添加属性类型
                propertySelect.appendChild(option);
            });
        }
    }

    // 设置属性选择框为当前 CODE type 相关的默认属性
    function setDefaultProperty() {
        var selectedType = codeTypeSelect.value;
        var options = propertySelect.options;

        for (var i = 0; i < options.length; i++) {
            var option = options[i];
            if (option.dataset.type === selectedType || option.dataset.type === '') {
                propertySelect.selectedIndex = i;
                break;
            }
        }
    }

    // 计算过期时间
    function calculateExpirationDate() {
        var selectedPropertyId = propertySelect.value;
        var expirationDate = new Date().toISOString();

        // 将数据发送到后端
        sendDataToBackend(expirationDate, selectedPropertyId);

        // 在前端显示过期时间
        displayExpirationDate(expirationDate);
    }

    // 将数据发送到后端
    function sendDataToBackend(expirationDate, selectedPropertyId) {
        var data = {
            expiration_date: expirationDate,
            property_id: selectedPropertyId
        };

        // 发送到后端的 AJAX POST 请求
        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/generate_code', true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.onload = function () {
            if (xhr.status === 200) {
                var response = JSON.parse(xhr.responseText);
                if (response.code) {
                    // 如果返回的注册信息中包含注册码，则显示在网页中
                    responseDataDiv.innerText = 'Registration Code: ' + response.code;
                } else {
                    console.error('未收到有效的注册信息。');
                }
            } else {
                console.error('生成注册码出错:', xhr.statusText);
            }
        };
        xhr.onerror = function () {
            console.error('生成注册码时发生网络错误。');
        };
        xhr.send(JSON.stringify(data));
    }

    // 在前端显示过期时间
    function displayExpirationDate(expirationDate) {
        // 可根据需要在界面上显示过期时间
        expirationDateResult.innerText = '过期时间: ' + expirationDate;
    }
});
