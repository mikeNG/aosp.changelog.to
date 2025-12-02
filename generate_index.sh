#!/bin/bash

script_dir="$(cd "$(dirname "$0")"; pwd -P)"
publish_dir="${script_dir}/../gh-pages"
output_file="$publish_dir/index.html"

function generate_version_divider() {
    local tab_id="$1"

    cat << EOF >> "$output_file"
                    </ul>
                </div>
                <div class="tab-pane" id="$tab_id">
                    <h2>Android $tab_id</h2>

                    <ul>
EOF
}

function generate_tag_list() {
    local version="$1"

    html_files=$(find "$publish_dir" -type f -name "*.html" -exec basename {} \; | grep "$version" | sed 's/-to-/:/' | sort -t : -k 2,2 -V | sed 's/:/-to-/')

    for file in $html_files; do
        second_tag=$(sed 's/.*-to-//' <<< "$file")
        second_tag="${second_tag%.html}"

        if [[ "$second_tag" == "$version"* ]]; then
            first_tag=$(sed 's/-to-.*//' <<< "$file")
            echo "                      <li><a href=\"$file\">$second_tag from $first_tag</a></li>" >> "$output_file"
        fi
    done
}

cat "${script_dir}/html_templates/index_header.html" > "$output_file"

generate_tag_list "android-16"
generate_tag_list "android-security-16"

generate_version_divider "15"
generate_tag_list "android-15"
generate_tag_list "android-security-15"

generate_version_divider "14"
generate_tag_list "android-14"
generate_tag_list "android-security-14"

generate_version_divider "13"
generate_tag_list "android-13"
generate_tag_list "android-security-13"

generate_version_divider "12L"
generate_tag_list "android-12.1"
generate_tag_list "android-security-12.1"

generate_version_divider "12"
generate_tag_list "android-12.0"
generate_tag_list "android-security-12.0"

generate_version_divider "11"
generate_tag_list "android-11"
generate_tag_list "android-security-11"

cat "${script_dir}/html_templates/index_footer.html" >> "$output_file"
