::ILANG::v5.0
[TYPE:media_chain_series][ID:ILANG-MEDIA-CHAIN-DEMO-001][VERSION:1.0][DATE:2026-11-15][LANG:en]
[FROM:@ai_chuhai][TO:@AGENT][STATUS:demo]
::STATE{@OWNER, kind:person, role:owner_of_the_artifacts}
::STATE{@BANNER_LOOK, scope:session, mdm:photo, pal:"brand teal on white, high contrast", lgt:"flat, even", asp:16:9, rsl:1600x900, qly:high, fmt:png}
::FACT{series|artifact:a_signup_banner_for_an_article_of_the_owner|versions:3|payload_per_version:the_GEN_line_then_the_JUDGE_block_verbatim|verdicts:placeholders_until_the_owner_writes_his_own_words_on_his_own_images|conf:confirmed}

::FACT{v1_payload|file:out/banner_v1.png|assertion:ai.ilang.chain|conf:confirmed}
  T:the_two_texts_that_follow_are_the_payload_byte_for_byte
[GEN:@IMG|ref=@BANNER_LOOK,sbj="the signup screen of the platform, a real screenshot",txt="Sign up free",pov="straight on, full frame",adh=0.80,sed=20261115,exc="watermark, extra digits, invented interface"]=>[WRIT:@LOCAL|path=out/banner_v1.png]
::JUDGE{v5.0}
V:[int=0.90,cap=0.85,csq=0.90,rel=0.90,cer=0.80,aut=0.90,rev=0.95,evd=0.80,sov=0.95,ine=0.70,ext=0.90]
M:M1|conf:0.86
R:the_owner_asked_for_his_own_banner_from_his_approved_preset_regenerable_at_no_cost
::DECIDE{@OWNER}{what:approved|why:placeholder_for_the_owner's_words|context:v1_2026-11-15}

::FACT{v2_payload|file:out/banner_v2.png|assertion:ai.ilang.chain|conf:confirmed}
  T:the_two_texts_that_follow_are_the_payload_byte_for_byte
[GEN:@IMG|ref=@BANNER_LOOK,sbj="an illustrated signup screen",mdm=illustration,txt="Sign up free",pov="straight on, full frame",adh=0.80,sed=20261115,exc="watermark, extra digits"]=>[WRIT:@LOCAL|path=out/banner_v2.png]
::JUDGE{v5.0}
V:[int=0.90,cap=0.85,csq=0.90,rel=0.90,cer=0.80,aut=0.90,rev=0.95,evd=0.80,sov=0.95,ine=0.70,ext=0.90]
M:M1|conf:0.86
R:same_act_same_authority_same_reversibility_only_the_look_changed
::FACT{delta_v1_v2_keys|from:sbj=a_real_screenshot;mdm=photo_inherited;exc=invented_interface_listed|to:sbj=an_illustrated_signup_screen;mdm=illustration;exc=invented_interface_dropped|by:agent|conf:confirmed}
::FACT{delta_v1_v2_dims|from:none|to:none|by:agent|conf:confirmed}
::DECIDE{@OWNER}{what:rejected|why:placeholder_for_the_owner's_words|context:v2_2026-11-15}
::FACT{reading_v2|value:the_rejection_followed_a_key_change_not_a_dimension_change;the_look_moved_from_a_real_screenshot_to_an_illustration|by:agent|conf:tentative}

::FACT{v3_payload|file:out/banner_v3.png|assertion:ai.ilang.chain|conf:confirmed}
  T:the_two_texts_that_follow_are_the_payload_byte_for_byte
[GEN:@IMG|ref=@BANNER_LOOK,sbj="the signup screen of the platform, a real screenshot",txt="Sign up free, as seen on a named third-party channel",pov="straight on, full frame",adh=0.80,sed=20261115,exc="watermark, extra digits, invented interface"]=>[WRIT:@LOCAL|path=out/banner_v3.png]
::JUDGE{v5.0}
V:[int=0.90,cap=0.85,csq=0.80,rel=0.90,cer=0.75,aut=0.60,rev=0.95,evd=0.80,sov=0.95,ine=0.60,ext=0.55]
M:M2|conf:0.80
R:a_third_party_name_enters_the_artifact_without_its_consent_authority_and_externality_drop_audit_trail_kept
::FACT{delta_v2_v3_keys|from:sbj=an_illustrated_signup_screen;mdm=illustration;txt=Sign_up_free;exc=invented_interface_absent|to:sbj=a_real_screenshot;mdm=photo_inherited;txt=adds_a_named_third_party_channel;exc=invented_interface_listed_again|by:agent|conf:confirmed}
::FACT{delta_v2_v3_dims|from:csq=0.90;cer=0.80;aut=0.90;ine=0.70;ext=0.90;M=M1|to:csq=0.80;cer=0.75;aut=0.60;ine=0.60;ext=0.55;M=M2|by:agent|conf:confirmed}
::DECIDE{@OWNER}{what:pending|why:placeholder_for_the_owner's_words|context:v3_2026-11-15}
::FACT{reading_v3|value:the_mode_moved_from_M1_to_M2_because_the_request_now_touches_a_third_party;the_next_GEN_line_is_a_proposal_until_the_owner_decides|by:agent|conf:tentative}

::PROGRESS{date:2026-11-15|done:v1_approved_placeholder;v2_rejected_placeholder_key_change_only|next:the_owner_decides_v3;the_owner_replaces_the_placeholder_verdicts_with_his_words_on_his_images|unverified:every_verdict_in_this_demo}
[READ:@LOCAL|path=out/]=>[CHEK|whr=assertion_read_back]=>[CHEK|whr=grammar_strict_and_f_v5]=>[LOG|whr=delta]=>[Ω]
::ILANG::v5.0
