WARNING: do not include this in release tarfile.

This note is for continuous intergration on travis (traditional build from source with 
extensive testing) and on circleci (conda and non-conda binary package build).
(There is a commit-checking-bot running on casegroup that checks new commit to amber repo
every 5 minutes. It will do a bunch of things and magic will happen)

Only serial AT is built.

You can always check status of each service by looking at the icons in

https://github.com/Amber-MD/ambertools-test/blob/nightly/README.md

How to check log?

GREEN: OK
RED: FAILED.

- circleci:
    - click its icon in above link or visit: https://circleci.com/gh/Amber-MD/ambertools-test/tree/nightly
    - click the build number (e.g: #159)
    - scroll down and look for "$ source devtools/ci/circleci_build.sh"
    - Since the build log is very long and circleci does not display all of them,
    you can download it by scroll down very end of the section, click "Download the full output as a file."

    circleci artifact (AmberTools*.tar.gz2) can be collected by running:
        python $AMBERHOME/AmberTools/src/download_circleci_AmberTools.py
    This artifact is being used by phenix build (and test) bot.

- travis:
    - click its icon in above link (README.md) or visit: https://travis-ci.org/Amber-MD/ambertools-test
    - click any of the build task that you're interested. I use TEST_TASK env to split the tests.
        - TEST_TASK="fast": testing all python stuff + related programs that might be useful for phenix
        - TEST_TASK="serial_MM" + TEST_TASK="serial_QMMM": testing sander serial
        - TEST_TASK="python": only testing Python packages
        - TEST_TASK="mmpbsa" or "rism": those tests are slow, so split them here.
    - You can download the log by clicking the link  for each build task, then click "Raw log"
        An example of that log (not sure how long travis keep it)
            https://s3.amazonaws.com/archive.travis-ci.org/jobs/207213712/log.txt
                You can search "file comparisons passed"
    If the tests failed, exit 1 --> travis job will be RED.

- email notification:

   add your email here if you want to get notification if the build failed:
       https://github.com/Amber-MD/ambertools-test/blob/nightly/.travis.yml#L47-L52

          notifications:
            email:
              recipients:
                - nhai.qn@gmail.com
              on_success: never # default: change
              on_failure: always # default: always

Note:

- If you do not want your small commit (fixing docs, README, ...) run on circleci or travis (save their computer
resources), you can add "[ci skip]" to your git commit
   e.g.: This is my message  "add README.ci.md for continuous intergration [ci skip]"
